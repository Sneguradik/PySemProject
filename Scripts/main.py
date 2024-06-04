import argparse
import logging
from GUI import SomeApp

def main():

    logger = logging.Logger("app")
    try:
        app = SomeApp()
        app.mainloop()

    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    main()
