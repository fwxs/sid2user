import winreg
import sys

__author__ = "pacmanator"
__email__ = "mrpacmanator at gmail dot com"
__version__ = "v1.0"


def get_normal_user_name(user_sid):
    """
        Return the name of a non-system user, based on it's sid.
        @param: user_sid: Windows user identifier.
    """
    user_name = None
    try:
        path = "{0}\\Volatile Environment".format(user_sid)
        with winreg.OpenKeyEx(winreg.HKEY_USERS, path) as key:
            user_name = winreg.QueryValueEx(key, "USERNAME")[0]
    
    except FileNotFoundError:
        pass
    
    except Exception as e:
        raise Exception(e)

    return user_name


def get_system_user_name(user_sid):
    """
        Return the name of a system user, based on it's sid.
        @param: user_sid: Windows user identifier.
    """
    user_name = None
    try:
        path = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList\\{0}".format(user_sid)
        with winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, path) as key:
            user_name = winreg.QueryValueEx(key, "ProfileImagePath")[0]

            # String index of the '\' character.
            inx = user_name.rfind("\\") + 1

            # Where does starts the name of the user.
            user_name = user_name[inx:]
    
    except FileNotFoundError:
        pass
    
    except Exception as e:
        raise Exception(e)

    return user_name


def get_user_name(user_sid):
    """
        Returns if the user sid belongs to a system user or to a non-system user.
        @param user_sid: Windows-user identification.
    """
    user_type, user_name = "Non-system", get_normal_user_name(user_sid)

    if user_name is None:
        user_type, user_name = "System", get_system_user_name(user_sid)
    
    return user_type, user_name


if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print("Usage: {0} <user_sid>", file=sys.stderr)
        sys.exit()
    
    user_type, user_name = get_user_name(sys.argv[1])

    if user_name is None:
        print("User doesn't exists", file=sys.stderr)
        sys.exit()

    print("[*] User name:", user_name)
    print("[*] User type:", user_type)
