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
  //states for pop up message
  const [popupMessage, setPopupMessage] = useState("");
  const [isPopupVisible, setIsPopupVisible] = useState(false);
  const navigate = useNavigate();


  const API_BASE_URL = process.env.REACT_APP_API_URL || '';

  const PopupMessage = ({ message, onClose }) => (
    <div className="popup-message">
      <div className="popup-content">
        <p>{message}</p>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );

  const handleCreateProject = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/create_project`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          projectName: projectName,
          projectId: projectId,
          description: projectDescription,
          userID: cookies.userID,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Project created:", data);
        setPopupMessage("Project created successfully!");
        setIsPopupVisible(true);
        fetchJoinedProjects();
      } else {
        const errorData = await response.json();
        setPopupMessage(`Failed to create project: ${errorData.message}`);
        setIsPopupVisible(true);
      }
    } catch (error) {
      console.error("Error:", error);
      setPopupMessage("Error: " + error);
      setIsPopupVisible(true);
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
        setPopupMessage("Successfully joined the project!");
        setIsPopupVisible(true);
        fetchJoinedProjects();
      } else if (response.status === 404) {
        setPopupMessage("Project not found. Please check the project ID.");
        setIsPopupVisible(true);
      } else if (response.status === 409) {
        setPopupMessage("You are already a member of this project.");
        setIsPopupVisible(true);
        setCookie("projectID", loginProjectId, { path: "/" });
      } else if (response.status === 500) {
        setPopupMessage("Server error occurred. Please try again later.");
        setIsPopupVisible(true);
      } else {
        setPopupMessage(data.message || "Failed to join project.");
        setIsPopupVisible(true);
      }
    } catch (error) {
      console.error("Error:", error);
      setPopupMessage("Network error occurred. Please check your connection.");
      setIsPopupVisible(true);
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
        setPopupMessage("Successfully left the project!");
        setIsPopupVisible(true);
        fetchJoinedProjects();
      } else if (response.status === 404) {
        setPopupMessage("Project not found. Please check the project ID.");
        setIsPopupVisible(true);
      } else if (response.status === 409) {
        setPopupMessage("You are not a member of this project.");
        setIsPopupVisible(true);
      } else if (response.status === 500) {
        setPopupMessage("Server error occurred. Please try again later.");
        setIsPopupVisible(true);
      } else {
        setPopupMessage(data.message || "Failed to leave project.");
        setIsPopupVisible(true);
      }
    } catch (error) {
      console.error("Error:", error);
      setPopupMessage("Network error occurred. Please check your connection.");
      setIsPopupVisible(true);
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
      {isPopupVisible && (
        <PopupMessage 
          message={popupMessage} 
          onClose={() => setIsPopupVisible(false)} 
        />
      )}
    </div>
  );
};

export default Projects;