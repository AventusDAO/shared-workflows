import sys
import os
import logging
import requests
import json


def vault_login(session, url, role_id, secret_id):
    data_input = {"role_id": role_id, "secret_id": secret_id}
    try:
        res = requests.post(F'https://{url}/v1/auth/approle/login', data=data_input)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    else:
        if res.status_code != 200:
            logging.error(F'Not able to log in {url}. Status code: {res.status_code})')
            sys.exit(1)
        json_res_output = json.loads(res.text)
        session.headers.update({"X-Vault-Token": json_res_output["auth"]["client_token"]})
        logging.info(F'Successfully logged in on {url}')


def get_vault_user(session, url, user_name):
    try:
        res = session.get(F'https://{url}/v1/avn-vault/user/{user_name}')
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    else:
        if res.status_code != 200:
            logging.error(F'Not able to fetch data from "{user_name}" in {url}. Status code: {res.status_code})')
            sys.exit(1)
        logging.info(F'"{user_name}" data successfully fetched from {url}')
    return res


def create_vault_payer(session, url, user_name, data):
    try:
        res = session.post(F'https://{url}/v1/avn-vault/user/set/{user_name}', data=data)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    else:
        if res.status_code != 200:
            logging.error(F'Not able to create the user "{user_name}" in {url}. Status code: {res.status_code})')
            sys.exit(1)
        logging.info(F'"{user_name}" successfully created in {url}')
    return


logging.basicConfig(format='(%(levelname)s) %(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

old_vault_session = requests.Session()
new_vault_session = requests.Session()
logging.info('Started vault sessions successfully')

vault_old_url = os.environ.get('vault_old_url')
vault_old_role_id = os.environ.get('vault_old_role_id')
vault_old_secret_id = os.environ.get('vault_old_secret_id')
vault_new_url = os.environ.get('vault_new_url')
vault_new_role_id = os.environ.get('vault_new_role_id')
vault_new_secret_id = os.environ.get('vault_new_secret_id')
list_vault_ids = os.environ.get('list_vault_ids').replace(" ", "").split(",")

vault_login(old_vault_session, vault_old_url, vault_old_role_id, vault_old_secret_id)
vault_login(new_vault_session, vault_new_url, vault_new_role_id, vault_new_secret_id)

logging.info('\n')
logging.info(F'verifying if "vault_ids" exist in old vault ({vault_old_url}):')
for vault_id in list_vault_ids:
    get_vault_user(old_vault_session, vault_old_url, F'GatewayPayer_{vault_id}')
logging.info(F'"vault_ids" verification in old vault ({vault_old_url}) finalized successfully\n')

logging.info(F'Starting migration of split fee payers to new eks vault ({vault_new_url}):')
for vault_id in list_vault_ids:
    user_data = json.loads(get_vault_user(old_vault_session, vault_old_url, F'GatewayPayer_{vault_id}').text)['data']
    create_vault_payer(new_vault_session, vault_new_url, F'GatewayPayer_{vault_id}', user_data)
logging.info(F'migration of split fee payers to new eks vault ({vault_new_url}) finalized successfully\n')

logging.info(F'Comparing split fee user data from both vault clusters:')
for vault_id in list_vault_ids:
    old_vault_data = json.loads(get_vault_user(old_vault_session, vault_old_url, F'GatewayPayer_{vault_id}').text)[
        "data"]
    new_vault_data = json.loads(get_vault_user(new_vault_session, vault_new_url, F'GatewayPayer_{vault_id}').text)[
        "data"]
    if sorted(old_vault_data.items()) != sorted(new_vault_data.items()):
        logging.error(F'GatewayPayer_{vault_id} user was not replicated correctly!')
logging.info(F'split fee user data comparison finalized successfully! All data replicated successfully!\n')
