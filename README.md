# library-api

Please build a simple library system for a school. With the following requirements:
There are many books in the library, and there are 1 or more copies of each title
Each student can borrow up to 10 books, and they need to be returned within 30 days. Within the 30 days they can renew once, and get another 30 days. And they can only renew the book once.

When student borrow/return a book, he/she will need to bring it to the librarian, and ask the librarian to register it in the system.

### There are 3 types of users:
Anyone (include anonymous), can check what book is in the library, and if they are available for borrowing:
1. if available, show how many copies are available for borrow
2. if not available, show when the book will be returned
### Student:
1. check what books he/she has borrowed, and what's the deadline to return it
2. if a book hasn't been renewed yet, the student can renew it
see a history of borrowed books
### Librarian:
1. can see which student borrowed which book, when to return, history of borrowing, etc
2. can mark a student borrowed a book
3. can mark a student returned a book

### swagger url:
- localhost:8000/schema/swagger-ui/

### admin page*
- localhost:8000/admin/

*please make admin account first