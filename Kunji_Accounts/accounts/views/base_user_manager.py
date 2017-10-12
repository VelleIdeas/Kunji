from abc import ABCMeta, abstractmethod


class BaseUserManager(object):
    '''
    All user management methods will be declared in this interface.
    '''

    __metaclass__ = ABCMeta

    @abstractmethod
    def populate_user(self, email):
        '''
        This method used to populate the user info

        :param email: email of the user
        :returns user object which contains user info
        '''
        pass


    @abstractmethod
    def create_user(self):
        '''
        This will handle below things:
        * adding user
        * adding user to related groups

        :param company: company object
        :returns user object
        '''
        pass

    @abstractmethod
    def update_user(self):
        '''
        This will handle below things:
        * update user data
        * update user groups which contains add/remove group
        * update company if required
        * update user email if required

        :param company: company object
        :returns added groups to that user
        '''
        pass


    @abstractmethod
    def is_new_user(self, email):
        '''
        This method is used to check given user is already exists or not

        :param email: email ID of the user
        :returns True if the user exists else returns False
        '''
        pass

    @abstractmethod
    def update_user_email(self, old_email, new_email):
        '''
        This method is used for update the user email

        :param old_email: current email of the user
        :param new_email: new email
        '''
        pass

    @abstractmethod
    def reset_user_password(self, email, new_password):
        '''
        This method is used for reset the user password

        :param email: email of the user
        :param new_password: new password
        '''
        pass

    @abstractmethod
    def remove_active_user_access(self, user, group):
        '''
        This method is used for reset the user password

        :param email: email of the user
        :param new_password: new password
        '''
        pass
