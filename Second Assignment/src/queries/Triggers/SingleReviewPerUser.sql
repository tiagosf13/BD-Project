-- Trigger will run to guarantee that each user can only have one review
-- On each product, if a new review is made, review is simply overwritten
CREATE TRIGGER dbo.SingleReviewPerUser on dbo.REVIEWS
INSTEAD OF INSERT
AS
BEGIN
    declare @userID as int;
    declare @productID as int;
    declare @reviewText as VARCHAR(255);
    declare @rating as int;
    declare @reviewDate as DATE;

    select @userID = user_id, @productID = product_id, 
           @reviewText = review_text, @rating = rating, 
           @reviewDate = review_date
    FROM inserted;

    declare @previousReviewID as int;
    SELECT @previousReviewID = review_id
    FROM REVIEWS
    WHERE user_id = @userID AND product_id = @productID

    IF (@previousReviewID is not NULL)
    BEGIN
        UPDATE REVIEWS
        SET review_text = @reviewText,
            rating = @rating, 
            review_date = @reviewDate
        WHERE review_id = @previousReviewID
    END
    ELSE
    BEGIN
        INSERT INTO reviews
        SELECT * FROM inserted;
    END
END