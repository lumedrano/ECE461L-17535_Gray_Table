import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import "./projects.scss";

const Projects = () => {
  const [projectName, setProjectName] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [projectId, setProjectId] = useState("");
  const [loginProjectId, setLoginProjectId] = useState("");
  const [cookies, removeCookie] = useCookies(['userID']);
  const navigate = useNavigate();


  const API_BASE_URL = process.env.APP_API_URL || 'http://127.0.0.1:5000';

  const handleCreateProject = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/create_project`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ projectName : projectName, projectId: projectId, description: projectDescription}),
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log("Project created:", data);
        alert("Project created successfully!");
        navigate("/hardware");
      } else {
        alert("Failed to create project.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error: " + error);
    }
  };
  
  const handleLoginProject = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/join_project`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId: cookies.userID, projectId: loginProjectId }),
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log("Joined project:", data);
        alert("Successfully joined the project!");
        navigate("/hardware");
      } else {
        alert("Failed to join project.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error: " + error);
    }
  };

  const handleLogout = () => {
    if (window.confirm("Are you sure you want to log out?")) {
      removeCookie('userID', { path: '/' });
      navigate('/');
    }
  };

  return (
    <div>
      <h2>Project Management</h2>
      <div className="logout-button-container">
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </div>
      <div className="columns">
        <div className="column project-management-area">
          <h3>Create New Project</h3>
          <div className="input-group">
            <input
              type="text"
              required
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
            />
            <label>Project Name</label>
          </div>
          <div className="input-group">
            <input
              type="text"
              required
              value={projectDescription}
              onChange={(e) => setProjectDescription(e.target.value)}
            />
            <label>Project Description</label>
          </div>
          <div className="input-group">
            <input
              type="text"
              required
              value={projectId}
              onChange={(e) => setProjectId(e.target.value)}
            />
            <label>Project ID</label>
          </div>
          <button onClick={handleCreateProject}>Create Project</button>
        </div>
      </div>
      <div className="existing-projects-area">
        <h3>Join Existing Project</h3>
        <div className="input-group">
          <input
            type="text"
            required
            value={loginProjectId}
            onChange={(e) => setLoginProjectId(e.target.value)}
          />
          <label>Project ID</label>
        </div>
        <button onClick={handleLoginProject}>Join Project</button>
      </div>
    </div>
  );  
};

export default Projects;