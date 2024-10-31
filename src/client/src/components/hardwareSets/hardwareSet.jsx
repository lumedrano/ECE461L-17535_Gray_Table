import React, {useEffect, useState} from "react";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import "./hardwareSet.scss"

const HardwareSets = () => {
    const [hardwareSets, setHardwareSets] = useState([]);
    const [newHardwareName, setNewHardwareName] = useState("");
    const [newHardwareCapacity, setNewHardwareCapacity] = useState("");
    const [projectName, setProjectName] = useState("");
    const [projectDescription, setProjectDescription] = useState("");
    const [projectId, setProjectId] = useState("");
    const [loginProjectId, setLoginProjectId] = useState("");
    const [cookies, removeCookie] = useCookies(['userID']);
    const navigate = useNavigate();

    const API_BASE_URL = process.env.APP_API_URL || 'http://127.0.0.1:5000';

    useEffect(() => {
        // Fetch hardware sets from the backend API using fetch instead of axios
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
        e.preventDefault(); // Prevent form submission default behavior

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
                setNewHardwareName(""); // Reset form fields
                setNewHardwareCapacity("");
                // Refresh the list of hardware sets
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

    return (
        <div className="hardware-sets">
            <h2>Hardware Sets</h2>

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
                            placeholder="Initial Capacity"  // Placeholder replaces the label
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