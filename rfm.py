import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextBrowser, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox

import mysql.connector

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Fill in your own information.
        self.database_connection = mysql.connector.connect(
            host="",
            user="",
            password="",
            database="crm"
        )

        self.setWindowTitle("RFM Database Operation Example")
        self.setGeometry(100, 100, 800, 600)

        title_style = "font-weight: bold; color: black; font-size: 16px; text-align: center;"

        self.add_title_label = QLabel("Data Addition Process", self)
        self.add_title_label.setStyleSheet(title_style)

        self.add_table_selector_label = QLabel("Select the table to add data to:")
        self.add_table_selector = QComboBox()
        self.add_table_selector.addItems([
            "rfm"
        ])

        self.add_value_input_labels = {}
        self.add_value_inputs = {}

        self.add_customer_id_label = QLabel("Customer ID:")
        self.add_customer_id_input = QLineEdit()

        self.add_button = QPushButton("Add Data")
        self.add_button.clicked.connect(self.add_to_database)

        self.delete_title_label = QLabel("Data Deletion Process", self)
        self.delete_title_label.setStyleSheet(title_style)

        self.delete_stockcode_input_label = QLabel("Enter the StockCode of the data to be deleted:")
        self.delete_stockcode_input = QLineEdit()
        self.delete_button = QPushButton("Delete Data")
        self.delete_button.clicked.connect(self.delete_from_database)

        self.view_title_label = QLabel("Data Viewing Process", self)
        self.view_title_label.setStyleSheet(title_style)

        self.view_table_selector_label = QLabel("Select the table to view:")
        self.view_table_selector = QComboBox()
        self.view_table_selector.addItems([
            "rfm"
        ])

        self.view_column_selector_label = QLabel("Select the column to view:")
        self.view_column_selector = QComboBox()
        self.view_column_selector.addItems([
            "Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price", "Country"
        ])

        self.view_button = QPushButton("View Data")
        self.view_button.clicked.connect(self.view_from_database)

        self.update_title_label = QLabel("Data Update Process", self)
        self.update_title_label.setStyleSheet(title_style)

        self.update_table_selector_label = QLabel("Select the table to update data in:")
        self.update_table_selector = QComboBox()
        self.update_table_selector.addItems([
            "rfm"
        ])

        self.update_stockcode_input_label = QLabel("Enter the StockCode of the data to update:")
        self.update_stockcode_input = QLineEdit()

        self.update_value_input_labels = {}
        self.update_value_inputs = {}

        self.update_customer_id_label = QLabel("New Customer ID:")
        self.update_customer_id_input = QLineEdit()

        self.update_button = QPushButton("Update Data")
        self.update_button.clicked.connect(self.update_database)

        main_layout = QHBoxLayout()

        form_layout = QFormLayout()
        form_layout.addRow(self.add_title_label)
        form_layout.addRow(self.add_table_selector_label, self.add_table_selector)

        selected_table = self.add_table_selector.currentText()
        cursor = self.database_connection.cursor()
        query = f"SHOW COLUMNS FROM {selected_table}"
        cursor.execute(query)
        columns = [column[0] for column in cursor.fetchall()]

        for column in columns:
            if column in ["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price", "Country"]:
                label = QLabel(f"{column}:")
                input_field = QLineEdit()
                self.add_value_input_labels[column] = label
                self.add_value_inputs[column] = input_field
                form_layout.addRow(label, input_field)

        form_layout.addRow(self.add_customer_id_label, self.add_customer_id_input)
        form_layout.addWidget(self.add_button)

        form_layout.addRow(self.delete_title_label)
        form_layout.addRow(self.delete_stockcode_input_label, self.delete_stockcode_input)
        form_layout.addWidget(self.delete_button)

        form_layout.addRow(self.view_title_label)
        form_layout.addRow(self.view_table_selector_label, self.view_table_selector)
        form_layout.addRow(self.view_column_selector_label, self.view_column_selector)
        form_layout.addWidget(self.view_button)

        form_layout.addRow(self.update_title_label)
        form_layout.addRow(self.update_table_selector_label, self.update_table_selector)
        form_layout.addRow(self.update_stockcode_input_label, self.update_stockcode_input)

        selected_table = self.update_table_selector.currentText()
        cursor = self.database_connection.cursor()
        query = f"SHOW COLUMNS FROM {selected_table}"
        cursor.execute(query)
        columns = [column[0] for column in cursor.fetchall()]

        for column in columns:
            if column in ["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price", "Country"]:
                label = QLabel(f"{column}:")
                input_field = QLineEdit()
                self.update_value_input_labels[column] = label
                self.update_value_inputs[column] = input_field
                form_layout.addRow(label, input_field)

        form_layout.addRow(self.update_customer_id_label, self.update_customer_id_input)
        form_layout.addWidget(self.update_button)

        main_layout.addLayout(form_layout)

        self.result_browser = QTextBrowser()
        self.result_browser.setStyleSheet("font-size: 12px;")
        self.result_browser.setReadOnly(True)
        main_layout.addWidget(self.result_browser)

        self.setLayout(main_layout)

    def add_to_database(self):
        selected_table = self.add_table_selector.currentText()

        columns = ["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price", "Country", "Customer_ID"]

        values = [
            self.add_value_inputs[column].text() or None for column in columns[:-1]
        ]

        customer_id_value = self.add_customer_id_input.text()
        if not customer_id_value:
            customer_id_value = None
        
        values.append(customer_id_value)

        cursor = self.database_connection.cursor()

        query = f"INSERT INTO {selected_table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
        cursor.execute(query, values)
        self.database_connection.commit()

        self.clear_result_browser()
        result_values = ', '.join([f"{column}={value}" for column, value in zip(columns, values)])
        self.result_browser.append(f"Data added to {selected_table} table: {result_values}")

    def delete_from_database(self):
        selected_table = self.add_table_selector.currentText()
        stockcode_to_delete = self.delete_stockcode_input.text()

        cursor = self.database_connection.cursor()
        query = f"DELETE FROM {selected_table} WHERE StockCode = %s"
        cursor.execute(query, (stockcode_to_delete,))
        self.database_connection.commit()

        self.clear_result_browser()
        self.result_browser.append(f"Data with StockCode {stockcode_to_delete} deleted from {selected_table} table.")

    def view_from_database(self):
        selected_table = self.view_table_selector.currentText()
        selected_column = self.view_column_selector.currentText()

        cursor = self.database_connection.cursor()
        query = f"SELECT {selected_column} FROM {selected_table}"
        cursor.execute(query)
        result = cursor.fetchall()

        result_text = f"Data in {selected_column} column of {selected_table} table:\n"
        for row in result:
            result_text += str(row) + "\n"
        self.result_browser.setText(result_text)

    def update_database(self):
        selected_table = self.update_table_selector.currentText()
        selected_stockcode = self.update_stockcode_input.text()
        selected_customer_id = self.update_customer_id_input.text()

        update_values = []
        update_data = []

        for column in self.update_value_input_labels:
            value = self.update_value_inputs[column].text()
            if value:
                update_values.append(f"{column} = %s")
                update_data.append(value)

        if selected_customer_id:
            update_values.append("Customer_ID = %s")
            update_data.append(selected_customer_id)

        if not update_values:
            self.result_browser.append("No values to update.")
            return

        update_values = ", ".join(update_values)

        cursor = self.database_connection.cursor()
        query = f"UPDATE {selected_table} SET {update_values} WHERE StockCode = %s"
        update_data.extend([selected_stockcode])
        cursor.execute(query, update_data)
        self.database_connection.commit()

        self.clear_result_browser()
        self.result_browser.append(f"Data in {selected_table} table updated.")

    def clear_result_browser(self):
        self.result_browser.clear()

    def closeEvent(self, event):
        self.database_connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())



'''
Importing the necessary libraries:
In the first step, I imported the necessary libraries for my program to run properly.
The sys library helped me manage system-related operations. At the same time, I laid the foundations for creating a user interface by adding widget classes from the PyQt5 library.
 I also included the mysql.connector library to provide a MySQL connection for database operations.

Creating the MyWindow Class:
Next, I created a class called MyWindow, which is a subclass derived from PyQt5's QWidget class.
The task of this class was to create and organize the main window of the application. At the same time, I created the necessary connection to connect to the MySQL database.

Design of Interface Elements:
Inside the MyWindow class, I designed the interface elements necessary for the user to perform database operations.
These elements were labels, input boxes, buttons and other user interaction elements. Through these elements, the user could add, delete and update data, as well as view the data.

Database Operations with Functions:
The add_to_database() function added new data to the MySQL database by allowing the user to add data.
delete_from_database() function deleted the data from the database. 
view_from_database() function allowed the user to view the data. 
update_database() function updated the data. 
These functions were executed as a result of user interaction.

Displaying and Closing Results:
A text browser called result_browser was used to display the results of the user's actions to the user. I didn't forget to close the database connection when the window was closed.

Main Program Flow:
I organized the flow of the main program in the __main__ section. I started PyQt5, set the theme and created a window from the MyWindow class, made it visible, started the application and entered the PyQt5 event loop.



In this way, I created a program that combines the user interface and MySQL database operations. Through the interface, users can add, delete and view data, as well as update data.
'''