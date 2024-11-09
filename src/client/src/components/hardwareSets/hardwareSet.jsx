import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import "./hardwareSet.scss";

const HardwareSets = () => {
    const [hardwareSets, setHardwareSets] = useState([]);
    const [newHardwareName, setNewHardwareName] = useState("");
    const [newHardwareCapacity, setNewHardwareCapacity] = useState("");
    const [selectedIndex, setSelectedIndex] = useState(-1);
    const API_BASE_URL = process.env.APP_API_URL || 'http://127.0.0.1:5000';

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

                if (response.ok && Array.isArray(data.message)) {
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
                alert("Hardware Set Created Successfully");
                setNewHardwareName("");
                setNewHardwareCapacity("");
                setHardwareSets([...hardwareSets, { name: newHardwareName, capacity: parseInt(newHardwareCapacity, 10), availability: parseInt(newHardwareCapacity, 10) }]);
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
                            placeholder="Initial Capacity"
                        />
                    </div>
                    <button type="submit" className="create-button">Create Hardware Set</button>
                </form>
            </div>

            <div className="hardware-list">
                <h3>Existing Hardware Sets</h3>
                {hardwareSets.length > 0 ? (
                    <div className="hardware-buttons">
                        {hardwareSets.map((set, index) => (
                            <button
                                key={index}
                                className={`hardware-button ${selectedIndex === index ? 'active' : ''}`}
                                onClick={() => setSelectedIndex(index)}
                            >
                                <h4>{set.hwName}</h4>
                                <p>Capacity: {set.capacity}</p>
                                <p>Availability: {set.availability}</p>
                            </button>
                        ))}
                    </div>
                ) : (
                    <p>No hardware sets available.</p>
                )}
            </div>
        </div>
    );
};

export default HardwareSets;
