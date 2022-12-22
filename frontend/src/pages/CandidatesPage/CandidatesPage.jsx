import React, { useEffect, useState } from 'react';
import axios from 'axios';
import useAuth from "../../hooks/useAuth";
import { Link } from "react-router-dom";

const CandidatesPage = () => {

    const [user, token] = useAuth();
    const [graduates, setGraduates] = useState([]);

    useEffect(() => {
        const fetchGraduates = async () => {
            try {
                let response = await axios.get('http://127.0.0.1:8000/api/auth/candidates/', {
                    headers: {
                        Authorization: "Bearer " + token,
                    },
                });
                setGraduates(response.data);
            } catch (error) {
                console.log('Error in set graduates', error);
            }
        };
        fetchGraduates();
    }, [token]);

    return (
        <><h1>Candidates for Graduation</h1>
            <h2>BACHELOR'S DEGREE PROGRAM</h2>
            <h2>128 CREDITS MINIMUM AND 3.0 GPA REQUIRED</h2>
            <h2><Link to="/employee">Back to Employee Portal</Link></h2>
            <br /><><><div className="container">
            {   graduates.map((graduate) => (
                <div key={graduate.id}>
                    <hr />
                    <span>LAST SEM: DEC |</span>
                    <span>EXP. GRAD: FEB |</span>
                    <span>{graduate.first_name} {graduate.last_name} |</span>
                    <span>GPA: {graduate.gpa} |</span>
                    <span><Link to="#" className="dummy">CR EARNED: {graduate.credits_earned} </Link></span>
                   </div>
                      ))}          
            </div><hr /><h2><Link to="#" className="dummy">Back to Top</Link></h2><div className="page-bottom"></div>
        </></></>
    );
};

export default CandidatesPage;

