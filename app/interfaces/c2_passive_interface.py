import abc
import os

from abc import ABC


class C2Passive(ABC):

    @property
    def display(self):
        return dict(name=self.name, description=self.description)

    @abc.abstractmethod
    def __init__(self, config):
        self.name = config['name']
        self.description = config['description']
        self.enabled = config['enabled']

    @abc.abstractmethod
    def valid_config(self):
        """
        Check whether the yaml file configuration is valid
        :return: True or False
        """
        return

    @abc.abstractmethod
    async def start(self):
        """
        Start the passive event loop for an additional C2 channel
        :return:
        """
        pass

    async def get_file(self, filename, platform):
        """
        Get file from file service and return file contents.

        :param filename: File name
        :param platform: File platform
        """
        if filename in self.file_svc.special_payloads:
            f = await self.file_svc.special_payloads[filename](dict(file=filename, platform=platform))
            return await self.file_svc.read_file(f)
        else:
            return await self.file_svc.read_file(filename)

    async def save_file(self, filename, payload, target_dir):
        """
        Save a file payload into the target_dir

        :param filename: Target file name
        :param payload: File contents
        :param target_dir: Final file path
        """
        try:
            with open(os.path.join(target_dir, filename), 'wb') as f:
                f.write(payload)
            self.log.debug('Uploaded file %s' % filename)
        except Exception as e:
            self.log.debug('Exception uploading file %s' % e)
