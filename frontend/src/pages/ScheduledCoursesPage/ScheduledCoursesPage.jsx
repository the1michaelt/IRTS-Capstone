import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import useAuth from "../../hooks/useAuth";


const ScheduledCoursesPage = () => {

    const [user, token] = useAuth();
    const [items, setItems] = useState([]);
    const [scheduledCourses, setScheduledCourses] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchItems = async () => {
            try {
                let response = await axios.get(`http://127.0.0.1:8000/api/student_courses/scheduled/`, {
                    headers: {
                        Authorization: "Bearer " + token,
                    },
                });
                console.log('Success response in ScheduledCourses', items)
                setItems(response.data);
            } catch (error) {
                console.log('Error in ScheduledCoursesPage', error);
            }
        };
    fetchItems();
    }, [token]);

    const fetchItems = async (courseId) => {
        let courseObject = {
            "course_id": courseId,
        }

        try {
            console.log('courseObject', courseObject)
            let response = await axios.post(`http://127.0.0.1:8000/api/student_courses/register_new_course/`,
                courseObject,
                {
                    headers: {
                        Authorization: "Bearer " + token,
                    },
                });

            console.log('Success response in items', courseId)
            setItems(response.data.items)
            navigate('/grades')
        } catch (error) {
            console.log('error in courseId', error.response.data)
        }

    };
    return (
            <><h1>Scheduled Courses for {user.first_name} {user.last_name}</h1>
                <h2>BACHELOR DEGREE PROGRAM</h2>
                <h2>COURSES ENROLLED: </h2>
                {/* <h2>TOTAL CREDITS ATTEMPTED: {sumAttemptedCredits}</h2> */}
                <br /><><><div>
                    {items.map((item) => (
                        <div key={item.id} className="container">
                            <hr />

                            <span>{item.course.name} | </span>
                            <span>DAYS: M, T, W | </span>
                            <span>CR VALUE: {item.course.credit_value} |</span>
                            <span>LOC: Online | </span>
                            <span>AUG - NOV | </span>
                        <div className="schedule-button">
                            <button type='submit' onClick={() => fetchItems(item.course.id)}>Add Grades</button>
                        </div>
                    </div>
                
                ))}

                {console.log('Return in item', items)}
            </div>
        </></></>
    );
};

export default ScheduledCoursesPage;
