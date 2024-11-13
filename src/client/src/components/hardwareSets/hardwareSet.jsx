import React, { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import { useAuth } from '../logincomponents/Auth';
import "./hardwareSet.scss";

const HardwareSets = () => {
    const [hardwareSets, setHardwareSets] = useState([]);
    const [newHardwareName, setNewHardwareName] = useState("");
    const [newHardwareCapacity, setNewHardwareCapacity] = useState("");
    //states for pop up message
    const [popupMessage, setPopupMessage] = useState("");
    const [isPopupVisible, setIsPopupVisible] = useState(false);
    const [loading, setLoading] = useState(false);
    const [cookies] = useCookies(["projectID"]);
    const projectID = cookies.projectID;
    const { logout } = useAuth();
    const API_BASE_URL = process.env.REACT_APP_API_URL || '';
    const navigate = useNavigate();


    const PopupMessage = ({ message, onClose }) => (
        <div className="popup-message">
          <div className="popup-content">
            <p>{message}</p>
            <button onClick={onClose}>Close</button>
          </div>
        </div>
      );

    const fetchHardwareSets = useCallback(async () => {
        setLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/fetch-hardware-sets`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ projectID })
            });
            const data = await response.json();
            if (response.ok) setHardwareSets(data.message);
            else console.error(`Error fetching hardware sets: ${data.message}`);
        } catch (error) {
            console.error("Error fetching hardware sets:", error);
        } finally {
            setLoading(false);
        }
    }, [API_BASE_URL, projectID]);

    useEffect(() => {
        fetchHardwareSets();
    }, [fetchHardwareSets]);

    const handleCreateHardwareSet = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${API_BASE_URL}/create_hardware_set`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    hwSetName: newHardwareName,
                    initCapacity: parseInt(newHardwareCapacity, 10),
                    projectID: projectID
                }),
            });
            const data = await response.json();
            if (response.ok) {
                setPopupMessage("Hardware Set Created Successfully");
                setIsPopupVisible(true);
                setNewHardwareName("");
                setNewHardwareCapacity("");
                fetchHardwareSets();
            } else {
                setPopupMessage(`Failed to create hardware set: ${data.message}`);
                setIsPopupVisible(true);
            }
        } catch (error) {
            setPopupMessage("An error occurred. Please try again.");
            setIsPopupVisible(true);
        }
    };

    const handleLogout = () => {
        if (window.confirm("Are you sure you want to log out?")) {
            logout();
        }
    };

    const handleGoBack = () => {
        navigate('/projects');
    };


    const handleCheckInOut = async (hwSetName, qty, action) => {
        // Validate quantity before making a request
        const parsedQty = parseFloat(qty);
        if (isNaN(parsedQty) || parsedQty <= 0) {
            setPopupMessage("Please enter a valid positive number for quantity.");
            setIsPopupVisible(true);
            return;
        }

        try {
            const endpoint = action === "check_in" ? "/check_in" : "/check_out";
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    hwSetName: hwSetName,
                    qty: parsedQty,
                }),
            });

            const data = await response.json();
            setPopupMessage(data.message); // Show the response message from the backend
            setIsPopupVisible(true);
            if (response.ok) {
                fetchHardwareSets(); // Re-fetch hardware sets to update the availability
            }
        } catch (error) {
            setPopupMessage("An error occurred. Please try again.");
            setIsPopupVisible(true);
        }
    };

    const handleDeleteHWSet = async (hwSetName) => {
        try {
            const response = await fetch(`${API_BASE_URL}/delete_hardware_set`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    hwSetName: hwSetName,
                    projectID: projectID
                }),
            });
            const data = await response.json();
            setPopupMessage(data.message); // Show the response message from the backend
            setIsPopupVisible(true);
            if (response.ok) {
                fetchHardwareSets(); // Re-fetch hardware sets to update the availability
            }
        } catch (error) {
            setPopupMessage("An error occurred. Please try again.");
            setIsPopupVisible(true);
        }
    };



    return (
        <div className="hardware-sets">
            <div className="header-section">
                <div className="logout-button-container">
                    <button onClick={handleLogout}>Logout</button>
                </div>
                <h2>Hardware Sets</h2>
                <div className="go-back-button-container">
                    <button onClick={handleGoBack}>Go Back to Projects</button>
                </div>
            </div>
    
            <div className="content-section">
                <div className="create-hardware-form">
                    <h3>Create New Hardware Set</h3>
                    <form onSubmit={handleCreateHardwareSet}>
                        <div className="input-group">
                            <input
                                type="text"
                                id="hardwareName"
                                value={newHardwareName}
                                onChange={(e) => setNewHardwareName(e.target.value)}
                                required
                                placeholder="Hardware Set Name"
                            />
                        </div>
                        <div className="input-group">
                            <input
                                type="number"
                                id="hardwareCapacity"
                                value={newHardwareCapacity}
                                onChange={(e) => setNewHardwareCapacity(e.target.value)}
                                required
                                placeholder="Initial Capacity"
                            />
                        </div>
                        <button type="submit">Create Hardware Set</button>
                    </form>
                </div>
    
                <div className="hardware-list">
                    <h3>Existing Hardware Sets</h3>
                    {loading ? (
                        <p>Loading hardware sets...</p>
                    ) : hardwareSets.length > 0 ? (
                        <div className="hardware-set-container">
                            {hardwareSets.map((set, index) => (
                                <div key={index} className="hardware-set-item">
                                    <h4>{set.hwName}</h4>
                                    <p><strong>Capacity:</strong> {set.capacity}</p>
                                    <p><strong>Availability:</strong> {set.availability}</p>
                                    <div className="hardware-action">
                                        <input
                                            type="number"
                                            placeholder="Quantity"
                                            id={`quantity-${set.hwName}`}
                                        />
                                        <button
                                            onClick={() => {
                                                const qty = document.getElementById(`quantity-${set.hwName}`).value;
                                                handleCheckInOut(set.hwName, qty, "check_in");
                                            }}
                                        >
                                            Check In
                                        </button>
                                        <button
                                            onClick={() => {
                                                const qty = document.getElementById(`quantity-${set.hwName}`).value;
                                                handleCheckInOut(set.hwName, qty, "check_out");
                                            }}
                                        >
                                            Check Out
                                        </button>
                                        <button
                                            onClick={() => handleDeleteHWSet(set.hwName)}
                                            className="delete-button"
                                        >
                                            Delete Set
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p>No hardware sets available.</p>
                    )}
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

export default HardwareSets;
