import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import "./projects.scss";

const Projects = () => {
  const [projectName, setProjectName] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [projectId, setProjectId] = useState("");
  const [loginProjectId, setLoginProjectId] = useState("");
  const [joinedProjects, setJoinedProjects] = useState(null); // New flag
  const [cookies, removeCookie] = useCookies(['userID']);
  const navigate = useNavigate();


  const API_BASE_URL = process.env.APP_API_URL || 'http://127.0.0.1:5000';

  const handleCreateProject = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/create_project`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          projectName: projectName, 
          projectId: projectId, 
          description: projectDescription,
          userID: cookies.userID 
        }),
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log("Project created:", data);
        alert("Project created successfully!");
        navigate("/hardware");
      } else {
        const errorData = await response.json();
        alert(`Failed to create project: ${errorData.message}`);
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
  
      const data = await response.json();
      
      if (response.ok) {
        console.log("Joined project:", data);
        alert("Successfully joined the project!");
        navigate("/hardware");
      } else if (response.status === 404) {
        alert("Project not found. Please check the project ID.");
      } else if (response.status === 409) {
        alert("You are already a member of this project.");
        navigate("/hardware");
      } else if (response.status === 500) {
        alert("Server error occurred. Please try again later.");
      } else {
        alert(data.message || "Failed to join project.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Network error occurred. Please check your connection.");
    }
  };

  const handleLogout = () => {
    if (window.confirm("Are you sure you want to log out?")) {
      removeCookie('userID', { path: '/' });
      navigate('/');
    }
  };
  const fetchJoinedProjects = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/get_user_projects_list`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ userId: cookies.userID }),
      });

      if (response.ok) {
        const data = await response.json();
        //setJoinedProjects(data.projects);
        setJoinedProjects(data.projects.length > 0 ? data.projects : []);
      } else {
        const errorData = await response.json();
        console.error("Error fetching projects:", errorData.message);
        setJoinedProjects([]);
      }
    } catch (error) {
      console.error("Error fetching projects:", error);
      setJoinedProjects([]);
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
        <h3>Use Existing Project</h3>
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
        <div className="joined-projects-area">
        <h3>Your Joined Projects</h3>
        <button onClick={fetchJoinedProjects}>Load Joined Projects</button>
        {joinedProjects !== null && (
          joinedProjects.length > 0 ? (
            <div className="project-list">
              {joinedProjects.map((projectId) => (
                <div key={projectId} className="project-item">
                  <p>Project ID: {projectId}</p>
                </div>
              ))}
            </div>
          ) : (
            <p>You have not joined any projects yet.</p>
          )
        )}
      </div>
      </div>
    </div>
  );  
};

export default Projects;