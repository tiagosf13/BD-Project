USE [p2g3];

DROP FUNCTION IF EXISTS getMonthlySalesTable
GO
-- OPTIONAL PARAMS month(int), year(int)
-- If month AND year are passed; then 
--      Returns a table with month-year total sale
-- Else If no parameters are passed
--      Returns table with overall sales divided monthly
CREATE FUNCTION getMonthlySalesTable(@month int = null, @year int = null)
RETURNS @monthlySales TABLE (
    year        int,
    month       int,
    total_sales  DECIMAL(10,2)
)
AS
BEGIN
    IF (@month is not null AND @year is not null)
    BEGIN
        INSERT INTO @monthlySales
        SELECT year, month, sum(total_price) as total_sales
        FROM (
            SELECT order_id,
                    YEAR(order_date) as year,
                    MONTH(order_date) as month,
                    total_price
            FROM ORDERS
        ) ordersMade
        GROUP BY year, month
        HAVING month=@month AND year=@year
    END

    ELSE
    BEGIN
        INSERT INTO @monthlySales
        SELECT year, month, sum(total_price) as total_sales
        FROM (
            SELECT order_id,
                    YEAR(order_date) as year,
                    MONTH(order_date) as month,
                    total_price
            FROM ORDERS
        ) ordersMade
        GROUP BY year, month
    END
    RETURN
END