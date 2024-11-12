import React, { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import { useAuth } from '../logincomponents/Auth';
import "./hardwareSet.scss";
import projects from "../projects/projects";

const HardwareSets = () => {
    const [hardwareSets, setHardwareSets] = useState([]);
    const [newHardwareName, setNewHardwareName] = useState("");
    const [newHardwareCapacity, setNewHardwareCapacity] = useState("");
    const [loading, setLoading] = useState(false);
    const [cookies] = useCookies(["userID", "projectId"]);
    const projectId = cookies.projectId;
    const { logout } = useAuth();
    const API_BASE_URL = process.env.APP_API_URL || 'http://127.0.0.1:5000';
    const navigate = useNavigate();

    const fetchHardwareSets = useCallback(async () => {
        setLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/fetch-hardware-sets`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ projectId })
            });
            const data = await response.json();
            if (response.ok) {
                console.log("Fetched Hardware Sets:", data.message);
                setHardwareSets(data.message);
            } else {
                console.error(`Error fetching hardware sets: ${data.message}`);
            }
        } catch (error) {
            console.error("Error fetching hardware sets:", error);
        } finally {
            setLoading(false);
        }
    }, [API_BASE_URL, projectId]);

    useEffect(() => {
        fetchHardwareSets();
    }, [fetchHardwareSets]);

    useEffect(() => {
    console.log("Current hardwareSets:", hardwareSets); // Log current state to verify
    }, [hardwareSets]);


const handleCreateHardwareSet = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
        const response = await fetch(`${API_BASE_URL}/create_hardware_set`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                hwSetName: newHardwareName,
                initCapacity: parseInt(newHardwareCapacity, 10),
                projectId: projectId
            }),
        });
        const data = await response.json();

        if (data.status === "success") {
            alert(data.message);
            setNewHardwareName("");
            setNewHardwareCapacity("");
            setHardwareSets((prevSets) => [
                ...prevSets,
                {
                    hwName: newHardwareName,
                    capacity: parseInt(newHardwareCapacity, 10),
                    availability: parseInt(newHardwareCapacity, 10),
                },
            ]);
            await fetchHardwareSets();
        } else {
            alert(`Failed to create hardware set: ${data.message}`)
        }
    } catch (error) {
        alert("An error occurred. Please try again.");
    } finally {
        setLoading(false);
    }
};

    const handleCheckInOut = async (hwSetName, qty, action) => {
        const parsedQty = parseFloat(qty);
        if (isNaN(parsedQty) || parsedQty <= 0) {
            alert("Please enter a valid positive number for quantity.");
            return;
        }
        setLoading(true);
        try {
            const endpoint = action === "check_in" ? "/check_in" : "/check_out";
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    projectId: projectId,
                    hwSetName: hwSetName,
                    qty: parsedQty,
                    userId: cookies.userID
                }),
            });

            const data = await response.json();
            alert(data.message);
            if (response.ok) {
                fetchHardwareSets();
            }
        } catch (error) {
            alert("An error occurred. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteHardwareSet = async (hwSetName) => {
        if (!window.confirm(`Are you sure you want to delete hardware set: ${hwSetName}?`)) {
            return;
        }
        setLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/delete_hardware_set`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    hwSetName: hwSetName,
                    projectId: projectId
                }),
            });
            const data = await response.json();
            alert(data.message);
            setHardwareSets((prevSets) => prevSets.filter((set) => set.hwName !== hwSetName));
            await fetchHardwareSets(); // Ensure data is re-fetched after deletion
            if (response.ok) {
                fetchHardwareSets();
            }
        } catch (error) {
            alert("An error occurred. Please try again.");
        } finally {
            setLoading(false);
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
                        <button type="submit" disabled={loading}>Create Hardware Set</button>
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
                                            disabled={loading}
                                        >
                                            Check In
                                        </button>
                                        <button
                                            onClick={() => {
                                                const qty = document.getElementById(`quantity-${set.hwName}`).value;
                                                handleCheckInOut(set.hwName, qty, "check_out");
                                            }}
                                            disabled={loading}
                                        >
                                            Check Out
                                        </button>
                                        <button
                                            onClick={() => handleDeleteHardwareSet(set.hwName)}
                                            className="delete-button"
                                            disabled={loading}
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
        </div>
    );
};

export default HardwareSets;
