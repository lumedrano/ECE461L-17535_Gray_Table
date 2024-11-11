import React, { useState , useEffect, useCallback} from "react";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import "./projects.scss";

const Projects = () => {
  const [projectName, setProjectName] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [projectId, setProjectId] = useState("");
  const [loginProjectId, setLoginProjectId] = useState("");
  const [joinedProjects, setJoinedProjects] = useState(null); 
  const [cookies, setCookie, removeCookie] = useCookies(['userID', 'projectID']);
  const navigate = useNavigate();


  const API_BASE_URL = process.env.REACT_APP_API_URL || '';

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
        // setCookie('projectID', projectId, { path: '/' });//set the cookies to the projectID passed to the body of request
        fetchJoinedProjects();
        // navigate("/hardware");
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
        // setCookie('projectID', loginProjectId, { path: '/' });//set the cookies to the projectID passed to the body of request
        fetchJoinedProjects();
        // navigate("/hardware");
      } else if (response.status === 404) {
        alert("Project not found. Please check the project ID.");
      } else if (response.status === 409) {
        alert("You are already a member of this project.");
        setCookie('projectID', loginProjectId, { path: '/' });//set the cookies to the projectID passed to the body of request
        // navigate("/hardware");
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

  const handleLeaveProject = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/leave_project`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId: cookies.userID, projectId: loginProjectId }),
      });
  
      const data = await response.json();
      
      if (response.ok) {
        console.log("Left project:", data);
        alert("Successfully left the project!");
        fetchJoinedProjects();
      } else if (response.status === 404) {
        alert("Project not found. Please check the project ID.");
      } else if (response.status === 409) {
        alert("You are not a member of this project.");
        setCookie('projectID', loginProjectId, { path: '/' });//set the cookies to the projectID passed to the body of request
      } else if (response.status === 500) {
        alert("Server error occurred. Please try again later.");
      } else {
        alert(data.message || "Failed to leave project.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Network error occurred. Please check your connection.");
    }
  };

  const handleLogout = () => {
    if (window.confirm("Are you sure you want to log out?")) {
      removeCookie('userID'); //handles the removal of cookies before logging out
      removeCookie('projectID');
      navigate('/');
    }
  };

  const handleProjectClick = (projectId) => {
    setCookie("projectID", projectId, { path: "/" });
    navigate("/hardware");
  };

  const fetchJoinedProjects = useCallback(async () => {
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
  }, [API_BASE_URL, cookies.userID]);

  useEffect(() => {
    fetchJoinedProjects();
  }, [fetchJoinedProjects]);

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
          <button onClick={handleLeaveProject}>Leave Project</button>
          <div className="joined-projects-area">
            <h3>Your Joined Projects</h3>
            {joinedProjects !== null && (
              joinedProjects.length > 0 ? (
                <div className="project-list">
                  {joinedProjects.map((projectId) => (
                    <button
                      key={projectId}
                      onClick={() => handleProjectClick(projectId)}
                      className="project-item"
                    >
                      Project ID: {projectId}
                    </button>
                  ))}
                </div>
              ) : (
                <p>You have not joined any projects yet.</p>
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Projects;