use bank;

CREATE TABLE loan_status_update (
    loan_id INT PRIMARY KEY
);

DELIMITER $$

CREATE TRIGGER record_loan_status_update
AFTER UPDATE ON bank_loan
FOR EACH ROW
BEGIN
    IF NEW.remaining_amount = 0 THEN
        INSERT INTO loan_status_update (loan_id)
        VALUES (NEW.loan_id)
        ON DUPLICATE KEY UPDATE loan_id = NEW.loan_id;
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE update_loan_status()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE loanId INT;
    DECLARE cur CURSOR FOR SELECT loan_id FROM loan_status_update;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO loanId;
        IF done THEN
            LEAVE read_loop;
        END IF;

        UPDATE bank_loan
        SET loan_status = '已还完'
        WHERE loan_id = loanId;
    END LOOP;

    CLOSE cur;

    DELETE FROM loan_status_update;
END$$

DELIMITER ;

DELIMITER $$

CREATE EVENT update_loan_status_event
ON SCHEDULE EVERY 0.5 MINUTE
DO
CALL update_loan_status()$$

DELIMITER ;