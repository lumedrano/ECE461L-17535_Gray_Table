import React from "react";
import "./projects/projects.scss";

function Project({name, desc, id}){
    return (
        <div class="project-container">
            <p className="project-id">{id}</p>
            <h2 className="project-name">{name}</h2>
            <p className="project-description">{desc}</p>
            <a href={`/projects/${id}`} className="project-visit">Visit</a>
        </div>
    );
}

export default Project;