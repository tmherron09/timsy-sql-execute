''' A Service class for handling of saving and reading data from %appdata% folder '''

import os
import json


class AppDataService:
    _backup_folder = 'Backup'
    _recovery_folder = 'Recovery'

    def __init__(self, app_name):
        self.app_name = app_name
        self.appdata_path = os.path.join(os.getenv('APPDATA'), app_name)
        if not os.path.exists(self.appdata_path):
            # TODO: Removed during testing - os.makedirs(self.appdata_path)
            print(self.appdata_path)
        self.appdata_local_path = os.path.join(os.getenv('LOCALAPPDATA'), app_name)
        if not os.path.exists(self.appdata_local_path):
            # TODO: Removed during testing - os.makedirs(self.appdata_local_path)
            print(self.appdata_local_path)

    def _init_appdata_folders(self):
        """ Create the appdata folders if they don't exist"""
        if not os.path.exists(self.appdata_path):
            # TODO: Removed during testing - os.makedirs(self.appdata_path)
            print(self.appdata_path)
        self.appdata_local_path = os.path.join(os.getenv('LOCALAPPDATA'), self.app_name)
        if not os.path.exists(self.appdata_local_path):
            # TODO: Removed during testing - os.makedirs(self.appdata_local_path)
            print(self.appdata_local_path)

    def _init_backup_folder(self):
        """
        Verify that the backup folder exists
        Create the backup folder if it doesn't exist
        """
        backup_folder = os.path.join(self.appdata_local_path, self._backup_folder)
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)

    def _init_recovery_folder(self):
        """
        Verify that the recovery folder exists
        Create the recovery folder if it doesn't exist
        """
        recovery_folder = os.path.join(self.appdata_local_path, self._recovery_folder)
        if not os.path.exists(recovery_folder):
            os.makedirs(recovery_folder)

    def save_user_data(self, filename, data):
        if not filename.endswith('.json'):
            filename += '.json'
        file_path = os.path.join(self.appdata_path, filename)
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def save_data(self, filename, data):
        file_path = os.path.join(self.appdata_path, filename)
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def save_backup(self, filename, data):

        self._init_backup_folder()
        if not filename.startswith('~'):
            filename = '~' + filename
        file_path = os.path.join(self.appdata_local_path, 'backup', filename)

    def write_recovery(self, filename, data):
        self._init_recovery_folder()
        if not filename.startswith('~'):
            filename = '~' + filename
        if not filename.endswith('.bak'):
            filename += '.bak'
        file_path = os.path.join(self.appdata_local_path, 'recovery', filename)

    def load_data(self, filename):
        file_path = os.path.join(self.appdata_path, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        else:
            return None

    def delete_data(self, filename):
        file_path = os.path.join(self.appdata_path, filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    def list_files(self):
        return os.listdir(self.appdata_path)


if __name__ == '__main__':
    # appdata_service = AppDataService('timsy_temp_service')
    print(os.getenv('LOCALAPPDATA'))
    lp = os.path.join(os.getenv('LOCALAPPDATA'), 'AppName', 'recovery', '~filename.json.bak')
    rp = os.path.join(os.getenv('LOCALAPPDATA'), 'AppName', 'recovery', '~filename', '.json')
    print(lp)
    print(rp)
    # env_vars = os.environ.keys()
    # for var in env_vars:
    #     print(var)
