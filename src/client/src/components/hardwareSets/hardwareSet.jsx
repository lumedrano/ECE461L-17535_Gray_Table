import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import { useLocation } from "react-router-dom";
import { useAuth } from "../logincomponents/Auth";
import "./hardwareSet.scss";

const HardwareSets = () => {
    const { state } = useLocation();
    const initialProjectId = state?.loginProjectId || "";
    const [loginProjectId] = useState(initialProjectId);
    const [hardwareSets, setHardwareSets] = useState([]);
    const [newHardwareName, setNewHardwareName] = useState("");
    const [newHardwareCapacity, setNewHardwareCapacity] = useState("");
    const [availabilityChange, setAvailabilityChange] = useState("");
    const [cookies] = useCookies(['userID']);
    const { logout } = useAuth();
    const navigate = useNavigate();

    //states for pop up message
  const [popupMessage, setPopupMessage] = useState("");
  const [isPopupVisible, setIsPopupVisible] = useState(false);

    const API_BASE_URL = process.env.REACT_APP_API_URL || '';


    const PopupMessage = ({ message, onClose }) => (
        <div className="popup-message">
          <div className="popup-content">
            <p>{message}</p>
            <button onClick={onClose}>Close</button>
          </div>
        </div>
      );

    useEffect(() => {
        const fetchHardwareSets = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/get_all_hw_sets`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                });

                const data = await response.json();
                if (response.ok) {
                    setHardwareSets(data.message);
                } else {
                    console.error(`Error fetching hardware sets: ${data.message}`);
                }
            } catch (error) {
                console.error("An error occurred while fetching hardware sets:", error);
            }
        };

        fetchHardwareSets();
    }, [API_BASE_URL]);

    const handleCreateHardwareSet = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch(`${API_BASE_URL}/create_hardware_set`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    hwSetName: newHardwareName,
                    initCapacity: parseInt(newHardwareCapacity, 10),
                }),
            });

            const data = await response.json();

            if (response.ok) {
                setPopupMessage("Hardware Set Created Successfully");
                setIsPopupVisible(true);
                setNewHardwareName("");
                setNewHardwareCapacity("");
                setHardwareSets([...hardwareSets, { hwName: newHardwareName, capacity: parseInt(newHardwareCapacity, 10), availability: parseInt(newHardwareCapacity, 10) }]);
            } else {
                console.error(`Error creating hardware set: ${data.message}`);
                setPopupMessage(`Failed to create hardware set: ${data.message}`);
                setIsPopupVisible(true);
            }
        } catch (error) {
            console.error("An error occurred while creating the hardware set:", error);
            setPopupMessage("An error occurred. Please try again.");
            setIsPopupVisible(true);
        }
    };

    const handleCheckOut = async (index) => {
        if (parseInt(availabilityChange) < 0) {
            setPopupMessage("Please enter a positive number.");
            setIsPopupVisible(true);
            return;
        }

        const selectedSet = hardwareSets[index];
        const hwName = selectedSet.hwName;

        try {
            const response = await fetch(`${API_BASE_URL}/check_out`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    projectId: loginProjectId,
                    hwSetName: hwName,
                    qty: parseInt(availabilityChange),
                    userId: cookies.userID
                }),
            });

            const data = await response.json();

            if (response.ok) {
                const updatedHardwareSets = hardwareSets.map((set, idx) => {
                    if (idx === index) {
                        return {
                            ...set,
                            availability: set.availability - parseInt(availabilityChange)
                        };
                    }
                    return set;
                });
                setHardwareSets(updatedHardwareSets);
                setPopupMessage("Checked Out Successfully");
                setIsPopupVisible(true);
            } else {
                console.error(`Error checking out space: ${data.message}`);
                setPopupMessage(`Error: ${data.message}`);
                setIsPopupVisible(true);
            }
        } catch (error) {
            console.error("An error occurred:", error);
            setPopupMessage("An error occurred. Please try again.");
            setIsPopupVisible(true);
        }
    };

    const handleCheckIn = async (index) => {
        if (parseInt(availabilityChange) < 0) {
            setPopupMessage("Please enter a positive number.");
            setIsPopupVisible(true);
            return;
        }

        const selectedSet = hardwareSets[index];
        const hwName = selectedSet.hwName;

        try {
            const response = await fetch(`${API_BASE_URL}/check_in`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    projectId: loginProjectId,
                    hwSetName: hwName,
                    qty: parseInt(availabilityChange),
                    userId: cookies.userID
                }),
            });

            const data = await response.json();

            if (response.ok) {
                const updatedHardwareSets = hardwareSets.map((set, idx) => {
                    if (idx === index) {
                        return {
                            ...set,
                            availability: set.availability + parseInt(availabilityChange)
                        };
                    }
                    return set;
                });
                setHardwareSets(updatedHardwareSets);
                setPopupMessage("Checked In Successfully");
                setIsPopupVisible(true);
            } else {
                console.error(`Error checking in space: ${data.message}`);
                setPopupMessage(`Error: ${data.message}`);
                setIsPopupVisible(true);
            }
        } catch (error) {
            console.error("An error occurred:", error);
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

    return (
        <div className="hardware-sets">
            <div className="header-section">
                <div className="logout-button-container">
                    <button onClick={handleLogout} className="logout-button">Logout</button>
                </div>
                <h2>Hardware Sets</h2>
                <div className="go-back-button-container">
                    <button onClick={handleGoBack} className="go-back-button">Go Back to Projects</button>
                    </div>
                </div>

                <div className="content-section">
                    <div className="create-hardware-form">
                        <h3>Create New Hardware Set</h3>
                        <form onSubmit={handleCreateHardwareSet}>
                            <div className="input-group">
                                <input
                                    type="text"
                                    value={newHardwareName}
                                    onChange={(e) => setNewHardwareName(e.target.value)}
                                    required
                                    placeholder="Hardware Set Name"
                                />
                            </div>
                            <div className="input-group">
                                <input
                                    type="number"
                                    value={newHardwareCapacity}
                                    onChange={(e) => setNewHardwareCapacity(e.target.value)}
                                    required
                                    placeholder="Initial Capacity"
                                />
                            </div>
                            <button type="submit" className="create-button">Create Hardware Set</button>
                        </form>
                    </div>

                    <div className="hardware-list">
                        <h3>Existing Hardware Sets</h3>
                        {hardwareSets.length > 0 ? (
                            <div className="hardware-set-container">
                                {hardwareSets.map((set, index) => (
                                    <div key={index} className="hardware-set-item">
                                        <h4>{set.hwName}</h4>
                                        <p>Capacity: {set.capacity}</p>
                                        <p>Availability: {set.availability}</p>
                                        <div className="hardware-action">
                                            <input
                                                type="number"
                                                value={availabilityChange}
                                                onChange={(e) => setAvailabilityChange(e.target.value)}
                                                placeholder="Quantity"
                                            />
                                            <button onClick={() => handleCheckIn(index)}>Check In</button>
                                            <button onClick={() => handleCheckOut(index)}>Check Out</button>
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