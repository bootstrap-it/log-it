import log_it
log = log_it.logger(__name__)

def test_log():
    log.debug("debug")
    log.info("info")

if __name__ == "__main__":
    test_log()