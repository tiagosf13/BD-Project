USE [BD-Project]
GO

-- OPTIONAL PARAMS month(int), year(int)
-- If month AND year are passed; then 
--      Returns a table with month-year total sale
-- Else If no parameters are passed
--      Returns table with overall sales divided monthly
CREATE FUNCTION getMonthlySalesTable(@month int = null, @year int = null)
RETURNS @monthlySales TABLE (
    month       int,
    year        int,
    totalSales  int
)
AS
BEGIN
    IF (@month is not null AND @year is not null)
    BEGIN
        INSERT INTO @monthlySales
        SELECT YEAR(order_date) as year,
                MONTH(order_date) as month,
                sum(total_price) as totalSales
        FROM ORDERS
        GROUP BY year, month
        HAVING month=@month AND year=@year
    END

    ELSE
    BEGIN
        INSERT INTO @monthlySales
        SELECT YEAR(order_date) as year,
                MONTH(order_date) as month,
                sum(total_price) as totalSales
        FROM ORDERS
        GROUP BY year, month
    END
    RETURN
END