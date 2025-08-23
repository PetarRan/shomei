"""
ASCII art and terminal messages for shomei.
"""

# Main logo (text-based)
SHOMEI_LOGO = """        

███████╗██╗  ██╗ ██████╗ ███╗   ███╗███████╗██╗
██╔════╝██║  ██║██╔═══██╗████╗ ████║██╔════╝██║
███████╗███████║██║   ██║██╔████╔██║█████╗  ██║
╚════██║██╔══██║██║   ██║██║╚██╔╝██║██╔══╝  ██║
███████║██║  ██║╚██████╔╝██║ ╚═╝ ██║███████╗██║
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝

"""

# Welcome message for first-time users
WELCOME_MESSAGE = """
welcome to shōmei! 🎉

bring your contributions from past jobs to your GitHub profile securely and privately.

what you can do:
• transform private commits into safe, public contributions.
• maintain your github activity graph.
• keep corporate code completely secure and show off your work.

ready to get started? 
run → shomei init
"""

# Installation success message
INSTALL_SUCCESS = """
🎉 shōmei has been successfully installed!

next steps:
1. initialize your configuration: shomei init
2. analyze a repository: shomei analyze /path/to/repo
3. process safely: shomei process /path/to/repo --dry-run

Need help? Run: shomei --help
Documentation: https://petarran.github.io/shomei/
"""

# Contributing message
CONTRIBUTING_MESSAGE = """
🤝 contributing to shōmei

we welcome contributions! here's how you can help:

• report bugs and feature requests
• improve documentation
• share your use cases and feedback

github: https://github.com/petarran/shomei
issues: https://github.com/petarran/shomei/issues

Every contribution helps make shōmei better for developers worldwide!
"""

# Safety reminder
SAFETY_REMINDER = """
⚠️  safety first!

remember:
• always use --dry-run first to preview changes
• review output before pushing to public repositories
• ensure no sensitive information remains
• follow your company's policies

shōmei is designed to protect you from leaking corporate IP, but always verify the results.
"""

# Version info
VERSION_INFO = """
shōmei v{version}
show off your coding contributions safely
"""

def get_logo(style="text"):
    """get the logo in the specified style."""
    return SHOMEI_LOGO

def get_welcome_message():
    """get the welcome message for new users."""
    return WELCOME_MESSAGE

def get_install_success():
    """get the installation success message."""
    return INSTALL_SUCCESS

def get_contributing_message():
    """get the contributing message."""
    return CONTRIBUTING_MESSAGE

def get_safety_reminder():
    """get the safety reminder."""
    return SAFETY_REMINDER

def get_version_info(version):
    """get version information."""
    return VERSION_INFO.format(version=version)

def print_logo(style="text"):
    """print the logo to stdout."""
    print(get_logo(style))

def print_welcome():
    """print the welcome message."""
    print(get_welcome_message())

def print_install_success():
    """print the installation success message."""
    print(get_install_success())

def print_contributing():
    """print the contributing message."""
    print(get_contributing_message())

def print_safety_reminder():
    """print the safety reminder."""
    print(get_safety_reminder())

def print_version_info(version):
    """print version information."""
    print(get_version_info(version))
