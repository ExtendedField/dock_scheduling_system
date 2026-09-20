Dev thoughts:

Step 1: Database
- Desgin DB system (sqllite) to house the legacy data and any new reservations
- Write script to move data from excel to db

Step 2: Scheduling logic
- Create new reservation API
- Search for reservation API?

Step 3: visualisation
- Build a React application as a view on this dataset
- User has to be able to
    - View current reservations in some kind of calendar format
    - Add a reservation
    - Delete a reservation

User Manual
- configure db password with an .env file