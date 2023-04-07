import site
site.addsitedir('/opt')

from awsmate import logger as al


def lambda_handler(raw_event, context):
    try:
        al.logger.info('Informational message')
        al.logger.warning('Warning message')    
        al.logger.error('Error message')

        raise RuntimeError("Crash!")

    except RuntimeError as err:
        al.log_internal_error('This is of course expected')
    