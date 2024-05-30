USE [p2g3];

DROP FUNCTION IF EXISTS searchAvailableProducts
GO

CREATE FUNCTION searchAvailableProducts (
    @searchTerm VARCHAR(255) = '%',
    @category VARCHAR(255) = '%',
    @minPrice int = 0,
    @maxPrice int = 1000000
) RETURNS TABLE
AS
RETURN (
    SELECT * 
    FROM Available_Products
    WHERE (product_name LIKE @searchTerm OR
           product_id LIKE @searchTerm) 
        AND category LIKE @category 
        AND price BETWEEN @minPrice AND @maxPrice
)