import React from "react";
import { useEffect, useState } from "react";
import useAuth from "../../hooks/useAuth";
import { Link } from "react-router-dom";
import './HomePage.css';
import axios from "axios";

const eeHomePage = () => {
  // The "user" value from this Hook contains the decoded logged in user information (username, first name, id)
  // The; "token" value is the JWT token that you will send in the header of any request requiring authentication
  //TODO: Add an AddCars Page to add a car for a logged in user's garage
  const [user, token] = useAuth();
  const [student, setStudent] = useState([]);
  // useEffect(() => {
  //   const fetchStudent= async () => {
  //     try {
  //       let response = await axios.get(`http://127.0.0.1:8000/api/student_courses/scheduled/`, {
  //         headers: {
  //           Authorization: "Bearer " + token,
  //         },
  //       });
  //       setStudent(response.data);
  //     } catch (error) {
  //       console.log(error.response.data);
  //     }
  //   };
  //   fetchStudent();
  // }, [token]); 
  return (
    <><div className="centered">
      <br /><h1>Welcome to the Employee Portal<br /> for Registration Services</h1><br />
      <Link to="/enrolled" className="register"> Directory of Current Students </Link>
    </div></>

  );
};
export default eeHomePage;