create database student_management;
use student_management;
CREATE TABLE Classes (
    class_id INT PRIMARY KEY AUTO_INCREMENT,
    class_name VARCHAR(50),
    section VARCHAR(5)
);
CREATE TABLE Students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    dob DATE,
    gender ENUM('Male', 'Female', 'Other'),
    contact VARCHAR(15),
    email VARCHAR(100),
    address TEXT,
    class_id INT,
    FOREIGN KEY (class_id) REFERENCES Classes(class_id)
);
CREATE TABLE Subjects (
    subject_id INT PRIMARY KEY AUTO_INCREMENT,
    subject_name VARCHAR(100) NOT NULL,
    max_marks INT NOT NULL
);
CREATE TABLE Teachers (
    teacher_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    subject_id INT,
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
);
CREATE TABLE Exams (
    exam_id INT PRIMARY KEY AUTO_INCREMENT,
    exam_name VARCHAR(50),
    exam_date DATE
);
CREATE TABLE Marks (
    marks_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    subject_id INT,
    exam_id INT,
    marks_obtained INT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id) ON DELETE CASCADE,
    FOREIGN KEY (exam_id) REFERENCES Exams(exam_id) ON DELETE CASCADE
);
desc marks;
desc classes;
desc students;
desc subjects;
desc teachers;
desc exams;

-- insert into classes values(301,"10","A");
-- insert into classes values(302,"10","B");

-- insert into Students values(1,"Ana",'2004-03-24','Female',
-- '9911111111','ana@gmail.com','house no. 2, sun colony, delhi',301);
-- insert into Students values(2,"Amit",'2004-06-04','Male',
-- '9911111112','amit@gmail.com','house no. 13, star colony, delhi',301);

-- insert into subjects values(501,"DBMS",100);
-- insert into subjects values(502,"OS",100);
-- insert into subjects values(503,"PP",100);
-- insert into subjects values(504,"DFS",100);

-- insert into teachers values(10,"Dr. Vaani",501);
-- insert into teachers values(11,"Dr. Swati",502);
-- insert into teachers values(12,"Dr. Neetu",503);
-- insert into teachers values(13,"Dr. Pankaj",504);

-- insert into exams values(1001,"Midterm",'2025-07-12');
-- insert into exams values(1002,"Final",'2025-09-30');

-- insert into marks values(001,1,501,1001,87);
-- insert into marks values(002,1,502,1001,83);
-- insert into marks values(003,1,503,1001,90);
-- insert into marks values(004,1,504,1001,89);

-- insert into marks values(005,2,501,1001,75);
-- insert into marks values(006,2,502,1001,80);
-- insert into marks values(007,2,503,1001,85);
-- insert into marks values(008,2,504,1001,78);

-- insert into marks values(009,1,501,1002,95);
-- insert into marks values(010,1,502,1002,90);
-- insert into marks values(011,1,503,1002,89);
-- insert into marks values(012,1,504,1002,94);

-- insert into marks values(013,2,501,1002,87);
-- insert into marks values(014,2,502,1002,93);
-- insert into marks values(015,2,503,1002,81);
-- insert into marks values(016,2,504,1002,93);

-- select * from students;

-- -- Step 1: Disable foreign key checks temporarily
-- SET FOREIGN_KEY_CHECKS = 0;
-- SET SQL_SAFE_UPDATES = 0;

-- -- Step 2: Clear data from child tables first, then parent tables
-- DELETE FROM Marks;
-- DELETE FROM Exams;
-- DELETE FROM Teachers;
-- DELETE FROM Subjects;
-- DELETE FROM Students;
-- DELETE FROM Classes;

-- -- Step 3: Re-enable foreign key checks
-- SET FOREIGN_KEY_CHECKS = 1;
-- SET SQL_SAFE_UPDATES = 1;
-- -- Step 4: Insert fresh dummy data

-- Classes
INSERT INTO Classes (class_id, class_name, section) VALUES
(301, '10', 'A'),
(302, '10', 'B'),
(303, '11', 'A');

-- Students
INSERT INTO Students (student_id, name, dob, gender, contact, email, address, class_id) VALUES
(1, 'Ana', '2004-03-24', 'Female', '9911111111', 'ana@gmail.com', 'House No. 2, Sun Colony, Delhi', 301),
(2, 'Amit', '2004-06-04', 'Male', '9911111112', 'amit@gmail.com', 'House No. 13, Star Colony, Delhi', 301),
(3, 'Riya', '2004-05-15', 'Female', '9911111113', 'riya@gmail.com', 'House No. 44, Green Park, Delhi', 302),
(4, 'Rohan', '2004-08-18', 'Male', '9911111114', 'rohan@gmail.com', 'House No. 18, Lake View, Delhi', 303);

-- Subjects
INSERT INTO Subjects (subject_id, subject_name, max_marks) VALUES
(501, 'DBMS', 100),
(502, 'Operating Systems', 100),
(503, 'Programming Principles', 100),
(504, 'Data Structures', 100),
(505, 'Computer Networks', 100);

-- Teachers
INSERT INTO Teachers (teacher_id, name, subject_id) VALUES
(10, 'Dr. Vaani', 501),
(11, 'Dr. Swati', 502),
(12, 'Dr. Neetu', 503),
(13, 'Dr. Pankaj', 504),
(14, 'Dr. Ramesh', 505);

-- Exams
INSERT INTO Exams (exam_id, exam_name, exam_date) VALUES
(1001, 'Midterm', '2025-07-12'),
(1002, 'Final', '2025-09-30');

-- Marks (Midterm + Final for each student)
INSERT INTO Marks (marks_id, student_id, subject_id, exam_id, marks_obtained) VALUES
(1, 1, 501, 1001, 85),
(2, 1, 502, 1001, 78),
(3, 1, 503, 1001, 88),
(4, 1, 504, 1001, 91),
(5, 1, 505, 1001, 82),

(6, 2, 501, 1001, 75),
(7, 2, 502, 1001, 80),
(8, 2, 503, 1001, 83),
(9, 2, 504, 1001, 79),
(10, 2, 505, 1001, 84),

(11, 3, 501, 1001, 88),
(12, 3, 502, 1001, 90),
(13, 3, 503, 1001, 92),
(14, 3, 504, 1001, 86),
(15, 3, 505, 1001, 85),

(16, 4, 501, 1001, 77),
(17, 4, 502, 1001, 73),
(18, 4, 503, 1001, 79),
(19, 4, 504, 1001, 82),
(20, 4, 505, 1001, 76),

-- Final Exam
(21, 1, 501, 1002, 92),
(22, 1, 502, 1002, 90),
(23, 1, 503, 1002, 95),
(24, 1, 504, 1002, 94),
(25, 1, 505, 1002, 89),

(26, 2, 501, 1002, 86),
(27, 2, 502, 1002, 88),
(28, 2, 503, 1002, 90),
(29, 2, 504, 1002, 83),
(30, 2, 505, 1002, 87),

(31, 3, 501, 1002, 94),
(32, 3, 502, 1002, 96),
(33, 3, 503, 1002, 91),
(34, 3, 504, 1002, 89),
(35, 3, 505, 1002, 93),

(36, 4, 501, 1002, 82),
(37, 4, 502, 1002, 79),
(38, 4, 503, 1002, 85),
(39, 4, 504, 1002, 80),
(40, 4, 505, 1002, 84);

select * from students;
select * from exams;
select * from marks;
select * from teachers;
select * from subjects;
select * from classes;

-- Classes
INSERT INTO Classes (class_id, class_name, section) VALUES
(301, '10', 'A'),
(302, '10', 'B');

-- Students
INSERT INTO Students (student_id, name, dob, gender, contact, email, address, class_id) VALUES
(1, 'Ana', '2004-03-24', 'Female', '9911111111', 'ana@gmail.com', 'House No. 2, Sun Colony, Delhi', 301),
(2, 'Amit', '2004-06-04', 'Male', '9911111112', 'amit@gmail.com', 'House No. 13, Star Colony, Delhi', 301),
(3, 'Reena', '2004-08-12', 'Female', '9911111113', 'reena@gmail.com', '45 Green Park, Delhi', 302),
(4, 'Rohit', '2004-10-22', 'Male', '9911111114', 'rohit@gmail.com', '88 Lake View, Delhi', 302);

-- Subjects
INSERT INTO Subjects (subject_id, subject_name, max_marks) VALUES
(501, 'DBMS', 100),
(502, 'OS', 100),
(503, 'PP', 100),
(504, 'DFS', 100);

-- Teachers
INSERT INTO Teachers (teacher_id, name, subject_id) VALUES
(10, 'Dr. Vaani', 501),
(11, 'Dr. Swati', 502),
(12, 'Dr. Neetu', 503),
(13, 'Dr. Pankaj', 504);

-- Exams
INSERT INTO Exams (exam_id, exam_name, exam_date) VALUES
(1001, 'Midterm', '2025-07-12'),
(1002, 'Final', '2025-09-30');

-- Marks (consistent with above)
INSERT INTO Marks (marks_id, student_id, subject_id, exam_id, marks_obtained) VALUES
(1, 1, 501, 1001, 87),
(2, 1, 502, 1001, 83),
(3, 1, 503, 1001, 90),
(4, 1, 504, 1001, 89),
(5, 2, 501, 1001, 75),
(6, 2, 502, 1001, 80),
(7, 2, 503, 1001, 85),
(8, 2, 504, 1001, 78),
(9, 3, 501, 1001, 82),
(10, 3, 502, 1001, 88),
(11, 3, 503, 1001, 79),
(12, 3, 504, 1001, 91),
(13, 4, 501, 1001, 69),
(14, 4, 502, 1001, 73),
(15, 4, 503, 1001, 77),
(16, 4, 504, 1001, 70),
(17, 1, 501, 1002, 95),
(18, 1, 502, 1002, 90),
(19, 1, 503, 1002, 89),
(20, 1, 504, 1002, 94),
(21, 2, 501, 1002, 87),
(22, 2, 502, 1002, 93),
(23, 2, 503, 1002, 81),
(24, 2, 504, 1002, 93);


-- adding more data
-- ---------------------------
use student_management;
-- Additional Students
-- ---------------------------
INSERT INTO Students (student_id, name, dob, gender, contact, email, address, class_id) VALUES
(5, 'Kiran', '2004-01-15', 'Male', '9911111115', 'kiran@gmail.com', '12 Park Street, Delhi', 301),
(6, 'Simran', '2004-02-20', 'Female', '9911111116', 'simran@gmail.com', '23 Rose Lane, Delhi', 301),
(7, 'Rahul', '2004-03-18', 'Male', '9911111117', 'rahul@gmail.com', '56 Green Street, Delhi', 302),
(8, 'Priya', '2004-04-25', 'Female', '9911111118', 'priya@gmail.com', '78 Lake Avenue, Delhi', 302),
(9, 'Sakshi', '2004-05-12', 'Female', '9911111119', 'sakshi@gmail.com', '89 Oak Street, Delhi', 301),
(10, 'Ankit', '2004-06-30', 'Male', '9911111120', 'ankit@gmail.com', '101 Pine Road, Delhi', 302);

-- ---------------------------
-- Additional Marks for New Students
-- ---------------------------
-- For Midterm Exam (1001)
INSERT INTO Marks (marks_id, student_id, subject_id, exam_id, marks_obtained) VALUES
(25, 5, 501, 1001, 78),
(26, 5, 502, 1001, 82),
(27, 5, 503, 1001, 74),
(28, 5, 504, 1001, 80),
(29, 6, 501, 1001, 88),
(30, 6, 502, 1001, 91),
(31, 6, 503, 1001, 85),
(32, 6, 504, 1001, 87),
(33, 7, 501, 1001, 69),
(34, 7, 502, 1001, 75),
(35, 7, 503, 1001, 72),
(36, 7, 504, 1001, 70),
(37, 8, 501, 1001, 84),
(38, 8, 502, 1001, 79),
(39, 8, 503, 1001, 88),
(40, 8, 504, 1001, 85),
(41, 9, 501, 1001, 92),
(42, 9, 502, 1001, 86),
(43, 9, 503, 1001, 90),
(44, 9, 504, 1001, 88),
(45, 10, 501, 1001, 77),
(46, 10, 502, 1001, 81),
(47, 10, 503, 1001, 79),
(48, 10, 504, 1001, 82);

-- For Final Exam (1002)
INSERT INTO Marks (marks_id, student_id, subject_id, exam_id, marks_obtained) VALUES
(49, 5, 501, 1002, 85),
(50, 5, 502, 1002, 89),
(51, 5, 503, 1002, 82),
(52, 5, 504, 1002, 87),
(53, 6, 501, 1002, 90),
(54, 6, 502, 1002, 94),
(55, 6, 503, 1002, 88),
(56, 6, 504, 1002, 91),
(57, 7, 501, 1002, 72),
(58, 7, 502, 1002, 77),
(59, 7, 503, 1002, 74),
(60, 7, 504, 1002, 78),
(61, 8, 501, 1002, 88),
(62, 8, 502, 1002, 82),
(63, 8, 503, 1002, 85),
(64, 8, 504, 1002, 87),
(65, 9, 501, 1002, 95),
(66, 9, 502, 1002, 91),
(67, 9, 503, 1002, 94),
(68, 9, 504, 1002, 92),
(69, 10, 501, 1002, 80),
(70, 10, 502, 1002, 84),
(71, 10, 503, 1002, 81),
(72, 10, 504, 1002, 85);

-- ---------------------------
-- Additional Students (Below Passing Marks)
-- ---------------------------
INSERT INTO Students (student_id, name, dob, gender, contact, email, address, class_id) VALUES
(11, 'Varun', '2004-07-10', 'Male', '9911111121', 'varun@gmail.com', '34 Maple Street, Delhi', 301),
(12, 'Meera', '2004-08-05', 'Female', '9911111122', 'meera@gmail.com', '56 Willow Lane, Delhi', 302);

-- ---------------------------
-- Marks Below Passing for Midterm Exam (1001)
-- ---------------------------
INSERT INTO Marks (marks_id, student_id, subject_id, exam_id, marks_obtained) VALUES
(73, 11, 501, 1001, 32),
(74, 11, 502, 1001, 28),
(75, 11, 503, 1001, 35),
(76, 11, 504, 1001, 30),
(77, 12, 501, 1001, 25),
(78, 12, 502, 1001, 38),
(79, 12, 503, 1001, 29),
(80, 12, 504, 1001, 33);

-- ---------------------------
-- Marks Below Passing for Final Exam (1002)
-- ---------------------------
INSERT INTO Marks (marks_id, student_id, subject_id, exam_id, marks_obtained) VALUES
(81, 11, 501, 1002, 30),
(82, 11, 502, 1002, 35),
(83, 11, 503, 1002, 32),
(84, 11, 504, 1002, 28),
(85, 12, 501, 1002, 29),
(86, 12, 502, 1002, 36),
(87, 12, 503, 1002, 31),
(88, 12, 504, 1002, 33);
