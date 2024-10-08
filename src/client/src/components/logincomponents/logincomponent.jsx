import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import "./logincomponent.scss";

const UserManagement = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [newUsername, setNewUsername] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [projectName, setProjectName] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [projectId, setProjectId] = useState("");
  const [loginProjectId, setLoginProjectId] = useState("");
  const [showNewUserPopup, setShowNewUserPopup] = useState(false);
  const navigate = useNavigate();
  const [cookies, setCookie] = useCookies(['userID']);

  const handleSignIn = async () => {
    try {
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (response.status === 200) {
        const data = await response.json();
        setCookie("userID", data.userID, { path: '/' });
        navigate("/projects");
      } else {
        alert("Login failed. Invalid credentials.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error: " + error);
    }
  };

  const handleCreateUser = async () => {
    try {
      const response = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: newUsername, password: newPassword }),
      });

      if (response.status === 201) {
        const data = await response.json();
        setCookie("userID", data.userID, { path: '/' });
        setShowNewUserPopup(false);
        navigate("/projects");
      } else {
        alert("Sign-up failed. User may already exist.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error: " + error);
    }
  };

  const handleCreateProject = async () => {
    // Implement project creation logic here
    console.log("Creating project:", { projectName, projectDescription, projectId });
  };

  const handleLoginProject = async () => {
    // Implement project login logic here
    console.log("Logging into project:", loginProjectId);
  };

  return (
    <div>
      <h2>User Management</h2>
      <div className="columns">
        <div className="column sign-in-area">
          <h3>Sign In</h3>
          <div className="input-group">
            <input
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <label>User ID</label>
          </div>
          <div className="input-group">
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <label>Password</label>
          </div>
          <button onClick={handleSignIn}>Sign In</button>
          <button onClick={() => setShowNewUserPopup(true)}>New User</button>
        </div>
        {showNewUserPopup && (
          <div className="column popup">
            <h3>Create New User</h3>
            <div className="input-group">
              <input
                type="text"
                required
                value={newUsername}
                onChange={(e) => setNewUsername(e.target.value)}
              />
              <label>New User ID</label>
            </div>
            <div className="input-group">
              <input
                type="password"
                required
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
              <label>New Password</label>
            </div>
            <button onClick={handleCreateUser}>Create User</button>
            <button onClick={() => setShowNewUserPopup(false)}>Close</button>
          </div>
        )}
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
        <h3>Login to Existing Projects</h3>
        <div className="input-group">
          <input
            type="text"
            required
            value={loginProjectId}
            onChange={(e) => setLoginProjectId(e.target.value)}
          />
          <label>Project ID</label>
        </div>
        <button onClick={handleLoginProject}>Login</button>
      </div>
    </div>
  );
};

export default UserManagement;