## SQL TABLES

### Supplier table

Unique ID PK (Increment NOT NULL)<br>
Unique Supplier Code - START WITH 401<br>
Name <br>
Optional Supplier Address <br>
Optional Supplier Mail <br>
Optional Supplier Phone <br>
Creation Time <br>

To add later : VAT KIND

### Customer table

Unique ID PK (Increment NOT NULL)<br>
Unique Customer Code - START WITH 411<br>
Name <br>
Optional Supplier Address <br>
Optional Supplier Mail <br>
Optional Supplier Phone <br>
Creation Time <br>

### Accounting Entry - Transaction Header

Unique ID PK (Increment NOT NULL)<br>
Optional Refered Invoice <br> 
Transaction Name <br>
Transaction Date <br>
Creation Time <br>


NEEDS TWO LINES

### Accounting Entry - Transaction Line (It's only one line)
Unique ID PK (Increment NOT NULL)<br>
FK - Transaction Header <br>
Type (Debit/Credit) <br>
Code  <br>
Amount <br>

### Account Table - To be imported ?

Unique ID PK (Increment NOT NULL)<br>
Account code <br> 
Account name <br>
Account type <br>


