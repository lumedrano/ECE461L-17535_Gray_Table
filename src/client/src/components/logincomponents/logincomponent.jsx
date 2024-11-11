import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import { useAuth } from "./Auth";
import { Eye, EyeOff } from "lucide-react";
import "./logincomponent.scss";

const UserManagement = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [userId, setUserId] = useState("");
  const [newUserId, setNewUserId] = useState("");
  const [newUsername, setNewUsername] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [showNewUserPopup, setShowNewUserPopup] = useState(false);
  
  // New state for password visibility
  const [showPassword, setShowPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  
  const navigate = useNavigate();
  const [cookies, setCookie] = useCookies(['userID']);
  const { login } = useAuth();

  const API_BASE_URL = process.env.REACT_APP_API_URL || '';

  const handleSignIn = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, userId, password }),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        setCookie("userID", data.userId, { path: '/' });
        login(data.userId);
        alert("Sign in was a success!")
        navigate("/projects");
      } else {
        alert(`Login failed: ${data.message}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while trying to log in.");
    }
  };
  
  const handleCreateUser = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/add_user`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: newUsername, userId: newUserId, password: newPassword }),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        setCookie("userID", data.userId, { path: '/' });
        login(data.userId);
        setShowNewUserPopup(false);
        alert("Sign up successful! You can now log in.");
      } else {
        alert(`Sign-up failed: ${data.message}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while trying to create a new user.");
    }
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
            <label>Username</label>
          </div>
          <div className="input-group">
            <input
              type="text"
              required
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
            />
            <label>User ID</label>
          </div>
          <div className="input-group password-input">
            <input
              type={showPassword ? "text" : "password"}
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <label>Password</label>
            <button 
              className="password-toggle"
              onClick={() => setShowPassword(!showPassword)}
              type="button"
            >
              {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
            </button>
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
              <label>New Username</label>
            </div>
            <div className="input-group">
              <input
                type="text"
                required
                value={newUserId}
                onChange={(e) => setNewUserId(e.target.value)}
              />
              <label>New User ID</label>
            </div>
            <div className="input-group password-input">
              <input
                type={showNewPassword ? "text" : "password"}
                required
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
              <label>New Password</label>
              <button 
                className="password-toggle"
                onClick={() => setShowNewPassword(!showNewPassword)}
                type="button"
              >
                {showNewPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
            <button onClick={handleCreateUser}>Create User</button>
            <button onClick={() => setShowNewUserPopup(false)}>Close</button>
          </div>
        )}
      </div>
    </div>
  );  
};

export default UserManagement;