from datetime import datetime
import getpass
import os


def clear_console():
    if os.name == 'nt':
        _ = os.system('cls')
    else: 
        _ = os.system('clear')
        

class User:
    def __init__(self, username, password, is_doctor=False):
        self.username = username
        self.password = password
        self.is_doctor = is_doctor
        self.appointments = []

    def add_appointment(self, appointment):
        self.appointments.append(appointment)

    def delete_appointment(self, index):
        if 1 <= index <= len(self.appointments):
            deleted_appointment = self.appointments.pop(index - 1)
            print(f"Appointment {index} deleted: {deleted_appointment}")
        else:
            print("Invalid appointment index. Please enter a valid index.")

    def confirm_appointment(self, index):
        if 1 <= index <= len(self.appointments):
            confirmed_appointment = self.appointments.pop(index - 1)
            print(f"Appointment confirmed: {confirmed_appointment}")
        else:
            print("Invalid appointment index. Please enter a valid index.")


class AppointmentApp:
    def __init__(self):
        self.users = {}
        self.doctors = {
            'Dr. Smith': ['Monday', 'Wednesday', 'Friday'],
            'Dr. Johnson': ['Tuesday', 'Thursday'],
            'Dr. Brown': ['Saturday', 'Sunday']
        }
        self.doctor_schedules = {
            'Dr. Smith': {'start_time': '08:30 AM', 'end_time': '11:30 AM'},
            'Dr. Johnson': {'start_time': '09:00 AM', 'end_time': '01:00 PM'},
            'Dr. Brown': {'start_time': '08:00 AM', 'end_time': '12:00 PM'}
        }

        
        for doctor_name in self.doctors.keys():
            self.users[doctor_name] = User(doctor_name, '123', is_doctor=True)

     
        self.doctor_appointments = {doctor: [] for doctor in self.doctors}

    def view_doctor_appointments(self, doctor_username):
        doctor_appointments = self.doctor_appointments.get(doctor_username, [])
        if doctor_appointments:
            print(f"\nAppointments for Dr. {doctor_username}")

            for index, appointment in enumerate(doctor_appointments, start=1):
                patient_username, appointment_datetime = appointment
                formatted_date = appointment_datetime.strftime('%A, %B %d, %Y')
                formatted_time = appointment_datetime.strftime('%I:%M %p')
                print(f"{index}. Patient: {patient_username}, Date: {formatted_date}, Time: {formatted_time}")

        else:
            print("\nNo appointments.")

    def display_menu(self):
        print("\nDoctor's Appointment")
        print("1. Log In as Doctor")
        print("2. Log In as Patient")
        print("3. Register as Patient")
        print("4. Exit")

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            if user.is_doctor:
                self.doctor_menu(username)
            else:
                self.patient_menu(username)
        else:
            print("\nInvalid username or password. Please try again")

    def patient_menu(self, username):
        while True:
            clear_console() 
            print(f"\nWelcome, {username}")
            print("1. View Appointments    -")
            print("2. Add Appointment      -")
            print("3. Delete Appointment   -")
            print("4. Log Out              -")

            choice = input("\nEnter your choice (1-4): ")
            clear_console() 

            if choice == '1':
                self.view_appointments(username)
                input("\nPress Enter to continue...")
            elif choice == '2':
                self.add_appointment(username)
                input("\nPress Enter to continue...")
            elif choice == '3':
                self.delete_appointment(username)
                input("\nPress Enter to continue...")
            elif choice == '4':
                print("\nLogging out. See you next time!")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 4.")


    def doctor_menu(self, username):
        while True:
            clear_console()  
            print(f"\nWelcome, {username}")
            print("1. View Appointments    -")
            print("2. Confirm Appointment  -")
            print("3. Log Out              -")

            choice = input("\nEnter your choice (1-3): ")
            clear_console() 

            if choice == '1':
                self.view_doctor_appointments(username)
                input("\nPress Enter to continue...")
            elif choice == '2':
                self.confirm_appointment(username)
                input("\nPress Enter to continue...")
            elif choice == '3':
                print("\nLogging out. See you next time!")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 3.")


    def register_patient(self):
        username = input("Enter your username: ")
        if username in self.users:
            print("\nUsername already exists. Please choose a different username.")
            return

        password = getpass.getpass("Enter your password: ")
        user = User(username, password)
        self.users[username] = user
        print("\nRegistration Successful!")

    def view_appointments(self, username):
        user = self.users.get(username)
        if user:
            user_appointments = user.appointments
            if not user_appointments:
                print("\nNo appointments yet.")
            else:
                print("\nYour Appointments")

                for index, appointment in enumerate(user_appointments, start=1):
                    doctor, appointment_datetime = appointment
                    formatted_date = appointment_datetime.strftime('%A, %B %d, %Y')
                    formatted_time = appointment_datetime.strftime('%I:%M %p')
                    print(f"{index}. Doctor: {doctor}, Date: {formatted_date}, Time: {formatted_time}")
        else:
            print("User not found.")

    def add_appointment(self, username):
        user = self.users.get(username)
        if user:
            print("\nChoose a doctor:")
        for i, (doctor, schedule) in enumerate(self.doctors.items(), start=1):
            print(f"{i}. {doctor} ({', '.join(schedule)})")
            print(f"   Schedule: {self.doctor_schedules[doctor]['start_time']} - {self.doctor_schedules[doctor]['end_time']}")

        try:
            doctor_index = int(input("Enter the number corresponding to the doctor: "))
            if 1 <= doctor_index <= len(self.doctors):
                selected_doctor = list(self.doctors.keys())[doctor_index - 1]

                date_str = input("Enter the appointment date (YYYY-MM-DD): ")
                try:
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                    day_of_week = date.strftime('%A')
                    if day_of_week in self.doctors[selected_doctor]:
                        time_str = input("Enter the appointment time (HH:MM AM/PM): ")
                        try:
                            time = datetime.strptime(time_str, '%I:%M %p').time()
                            if self.is_valid_time(selected_doctor, time):
                                appointment_datetime = datetime.combine(date.date(), time)
                                appointment = (selected_doctor, appointment_datetime) 

                                
                                self.doctor_appointments[selected_doctor].append((username, appointment_datetime))

                                
                                user.add_appointment((selected_doctor, appointment_datetime))

                                print("\nAppointment added successfully")
                            else:
                                print(f"\nInvalid time. Please select a time between "
                                      f"{self.doctor_schedules[selected_doctor]['start_time']} and "
                                      f"{self.doctor_schedules[selected_doctor]['end_time']}")
                        except ValueError:
                            print("\nInvalid time format. Please enter in 'HH:MM AM/PM' format")
                    else:
                        print(f"\nThe selected doctor is not available on {day_of_week}. Please choose another day.")
                except ValueError:
                    print("\nInvalid date format. Please enter in 'YYYY-MM-DD' format")
            else:
                print("\nInvalid doctor selection. Please enter a valid number.")
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")            


    def delete_appointment(self, username):
        user = self.users.get(username)
        if user:
            if not user.appointments:
                print("\nNo appointments to delete.")
                return

            print("== Your Appointments ==")

            for index, appointment in enumerate(user.appointments, start=1):
                doctor, appointment_datetime = appointment
                formatted_date = appointment_datetime.strftime('%A, %B %d, %Y')
                formatted_time = appointment_datetime.strftime('%I:%M %p')
                print(f"{index}. Doctor: {doctor}, Date: {formatted_date}, Time: {formatted_time}")

            try:
                appointment_index = int(input("Enter the appointment index to delete: "))
                if 1 <= appointment_index <= len(user.appointments):
                    user.delete_appointment(appointment_index)
                else:
                    print("\nInvalid appointment index. Please enter a valid index.")
            except ValueError:
                print("\nInvalid input. Please enter a valid number.")
        else:
            print("User not found.")

    def confirm_appointment(self, doctor_username):
      doctor_appointments = self.doctor_appointments.get(doctor_username, [])
      if doctor_appointments:
          print(f"\nAppointments for Dr. {doctor_username}")

          for index, appointment in enumerate(doctor_appointments, start=1):
              patient, appointment_datetime = appointment
              formatted_datetime = appointment_datetime.strftime('%A, %B %d, %Y at %I:%M %p')
              print(f"{index}. Patient: {patient}, Appointment: {formatted_datetime}")

          try:
              appointment_index = int(input("Enter the appointment index to confirm: "))
              if 1 <= appointment_index <= len(doctor_appointments):
                  confirmed_appointment = doctor_appointments.pop(appointment_index - 1)
                  formatted_date = confirmed_appointment[1].strftime('%A, %B %d, %Y')
                  formatted_time = confirmed_appointment[1].strftime('%I:%M %p')
                  print(f"Appointment confirmed: Patient: {confirmed_appointment[0]}, Date: {formatted_date}, Time: {formatted_time}")
              else:
                  print("\nInvalid appointment index. Please enter a valid index.")
          except ValueError:
              print("\nInvalid input. Please enter a valid number.")
      else:
          print("\nNo appointments to confirm.")


    def is_valid_time(self, doctor, appointment_time):
        start_time = datetime.strptime(self.doctor_schedules[doctor]['start_time'], '%I:%M %p').time()
        end_time = datetime.strptime(self.doctor_schedules[doctor]['end_time'], '%I:%M %p').time()
        return start_time <= appointment_time <= end_time


def main():
    appointment_app = AppointmentApp()

    while True:
        clear_console()  
        appointment_app.display_menu()
        choice = input("Enter your choice (1-4): ")
        clear_console() 

        if choice == '1':
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")
            appointment_app.login(username, password)
            clear_console() 
        elif choice == '2':
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")
            appointment_app.login(username, password)
            clear_console()  
        elif choice == '3':
            appointment_app.register_patient()
            clear_console()  
        elif choice == '4':
            print("\nExiting the Doctor's Appointment Application. Good bye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")



if __name__ == "__main__":
    main()