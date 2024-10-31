import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import { useCookies } from "react-cookie";
import { useAuth } from '../logincomponents/Auth'; // Import Auth context
import "./hardwareSet.scss";

const HardwareSets = () => {
    const [hardwareSets, setHardwareSets] = useState([]);
    const [newHardwareName, setNewHardwareName] = useState("");
    const [newHardwareCapacity, setNewHardwareCapacity] = useState("");
    const { logout } = useAuth();  // Use logout from AuthProvider

    const API_BASE_URL = process.env.APP_API_URL || 'http://127.0.0.1:5000';

    // Initialize useNavigate here
    const navigate = useNavigate(); 

    useEffect(() => {
        const fetchHardwareSets = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/get_all_hw_names`, {
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
    }, []);

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
                alert("Hardware Set Created Successfully");
                setNewHardwareName("");
                setNewHardwareCapacity("");
                setHardwareSets([...hardwareSets, newHardwareName]);
            } else {
                console.error(`Error creating hardware set: ${data.message}`);
                alert(`Failed to create hardware set: ${data.message}`);
            }
        } catch (error) {
            console.error("An error occurred while creating the hardware set:", error);
            alert("An error occurred. Please try again.");
        }
    };

    const handleLogout = () => {
        if (window.confirm("Are you sure you want to log out?")) {
            logout(); // Trigger full logout
        }
    };

    // Handle navigation back to projects page
    const handleGoBack = () => {
        navigate('/projects'); // Navigate to the projects page
    };

    return (
        <div className="hardware-sets">
            <div className="logout-button-container">
                <button onClick={handleLogout}>Logout</button>
            </div>

            <h2>Hardware Sets</h2>

            {/* Go Back Button */}
            <div className="go-back-button-container">
                <button onClick={handleGoBack}>Go Back to Projects</button>
            </div>

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
                {hardwareSets.length > 0 ? (
                    <ul>
                        {hardwareSets.map((set, index) => (
                            <li key={index}>{set}</li>
                        ))}
                    </ul>
                ) : (
                    <p>No hardware sets available.</p>
                )}
            </div>
        </div>
    );
};

export default HardwareSets;
