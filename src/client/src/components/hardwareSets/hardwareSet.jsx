import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import "./hardwareSet.scss"

const HardwareSets = () => {
    const [projectName, setProjectName] = useState("");
    const [projectDescription, setProjectDescription] = useState("");
    const [projectId, setProjectId] = useState("");
    const [loginProjectId, setLoginProjectId] = useState("");
    const [cookies, removeCookie] = useCookies(['userID']);
    const navigate = useNavigate();

    const API_BASE_URL = process.env.APP_API_URL || 'http://127.0.0.1:5000';

    return (
        <div>
            <h2>Hardware</h2>
        </div>
    )

}

export default HardwareSets;