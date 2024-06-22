USE bank;
DELIMITER //

CREATE FUNCTION customer_assets(in_customer_id VARCHAR(32))
RETURNS JSON
READS SQL DATA
BEGIN
    DECLARE total_balance DECIMAL(15, 2);
    DECLARE total_loan DECIMAL(15, 2);
    DECLARE net_assets DECIMAL(15, 2);
    DECLARE result JSON;

    -- 查询客户所有账户的余额总和
    SELECT COALESCE(SUM(current_balance), 0) INTO total_balance
    FROM bank_account
    WHERE customer_id = in_customer_id;

    -- 查询客户所有账户下贷款的总和
    SELECT COALESCE(SUM(loan_amount), 0) INTO total_loan
    FROM bank_loan
    WHERE account_id IN (SELECT account_number FROM bank_account WHERE customer_id = in_customer_id);

    -- 计算净资产
    SET net_assets = total_balance - total_loan;

    -- 组合结果为JSON
    SET result = JSON_OBJECT(
        'total_balance', total_balance,
        'total_loan', total_loan,
        'net_assets', net_assets
    );

    RETURN result;
END //

DELIMITER ;