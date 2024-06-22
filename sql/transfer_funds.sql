USE bank;
DELIMITER //

CREATE PROCEDURE transfer_funds(
   IN from_account_number VARCHAR(20),
   IN to_account_number VARCHAR(20),
   IN amount DECIMAL(10, 2)
)
BEGIN
   DECLARE from_balance DECIMAL(10, 2);
   DECLARE to_balance DECIMAL(10, 2);

   -- 检查转出账户是否存在
   SELECT current_balance INTO from_balance FROM bank_account WHERE account_number = from_account_number;
   IF from_balance IS NULL THEN
	   SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '转出账户ID不存在。';
   END IF;

   -- 检查转入账户是否存在
   SELECT current_balance INTO to_balance FROM bank_account WHERE account_number = to_account_number;
   IF to_balance IS NULL THEN
	   SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '转入账户ID不存在。';
   END IF;

   -- 检查转出账户余额是否足够
   IF from_balance < amount THEN
	   SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '转出账户余额不足。';
   END IF;

   -- 扣减转出账户余额
   UPDATE bank_account SET current_balance = current_balance - amount WHERE account_number = from_account_number;

   -- 增加转入账户余额
   UPDATE bank_account SET current_balance = current_balance + amount WHERE account_number = to_account_number;
END //

DELIMITER ;