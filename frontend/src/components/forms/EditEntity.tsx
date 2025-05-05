import { useState } from "react";
import { DHFC_Entity } from "../../types";
import { useDocumentContext } from "../DocumentProvider";
import EditAssertion, { isAssertionValid } from "./EditAssertion";

export function isEntityValid(entity: DHFC_Entity): boolean {
    return (
        entity.name.trim() !== '' &&
        entity.type_uri.trim() !== '' &&
        entity.assertions.length > 0 &&
        entity.assertions.every(assertion => isAssertionValid(assertion))
    );
}

export default function EditEntity({ entity, onChange, onSuppr }: { entity: DHFC_Entity, onChange: (entity: DHFC_Entity) => void, onSuppr: () => void }) {
    const [entityData, setEntityData] = useState<DHFC_Entity>(entity);
    const { domain_ontology } = useDocumentContext();

    const classes = Object.keys(domain_ontology.classes).filter(c => domain_ontology.classes[c].length > 0);
    const class_name = (class_uri: string) => {
        const parts = class_uri.split("#");
        return parts[parts.length - 1];
    }

    const setEntityDataWithChanges = (changes: (prev: DHFC_Entity) => DHFC_Entity) => {
        setEntityData(changes);
        onChange(entityData);
    }

    const changeEntityType = (newType: string) => {
        setEntityDataWithChanges(prev => ({
            ...prev,
            type_uri: newType,
        }));
    }

    const changeEntityAssertion = (newAssertion: any, index: number) => {
        setEntityDataWithChanges(prev => ({
            ...prev,
            assertions: prev.assertions.map((assertion, i) => i === index ? newAssertion : assertion)
        }));
    }

    const supprAssertion = (index: number) => {
        setEntityDataWithChanges(prev => ({
            ...prev,
            assertions: prev.assertions.filter((_, i) => i !== index)
        }));
    }

    const addAssertion = () => {
        setEntityDataWithChanges(prev => ({
            ...prev,
            assertions: [...prev.assertions, { property_uri: "", object_name: "" }]
        }));
    }

    return (
        <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <label htmlFor="type">Type:</label>
                <select
                    id="type"
                    value={entityData.type_uri}
                    onChange={(e) => { changeEntityType(e.target.value) }}
                >
                    <option value="">Select a type</option>
                    {classes.map(class_name).map((className) => (
                        <option value={className}>
                            {className}
                        </option>
                    ))}
                </select>
                <label htmlFor="name">Nom:</label>
                <input
                    id="name"
                    type="text"
                    value={entityData.name}
                    onChange={(e) => { changeEntityType(e.target.value) }}
                />
                <button onClick={onSuppr}>Supprimer</button>
            </div>
            <div style={{ marginLeft: "20px" }}>
                {entityData.assertions.map((assertion, index) => (
                    <EditAssertion
                        assertion={assertion}
                        class_uri={entityData.type_uri}
                        onChange={(newAssertion) => changeEntityAssertion(newAssertion, index)}
                        onSuppr={() => supprAssertion(index)}
                    />
                ))}
                <button onClick={addAssertion}>Ajouter une assertion</button>
            </div>
        </div>
    )
}