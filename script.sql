/*
 * This script execute the "sparkling water" example.
 */

DO $$
DECLARE 
  client integer;
  firstOrder integer;
  ticket RECORD;
  secondOrder integer;
  tablePaid RECORD;
BEGIN
  -- The client acquire the second table and we get the client token.
  SELECT INTO client AcquireTable(20);

  -- The client orders a sparkling water.
  SELECT INTO firstOrder OrderDrinks(client,ARRAY[[2,1]]);

  -- The client then looks at his bill.
  SELECT INTO ticket IssueTicket(client);

  -- The client then order another sparkling water.
  SELECT INTO secondOrder OrderDrinks(client,ARRAY[[2,1]]);

  -- Finally, the client pays and release the table.
  SELECT INTO tablePaid PayTable(client,4);
END $$;