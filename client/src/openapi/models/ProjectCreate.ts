/* tslint:disable */
/* eslint-disable */
/**
 * Marron API
 * API of Marron
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface ProjectCreate
 */
export interface ProjectCreate {
    /**
     * 
     * @type {string}
     * @memberof ProjectCreate
     */
    name: string;
    /**
     * 
     * @type {string}
     * @memberof ProjectCreate
     */
    description: string;
    /**
     * 
     * @type {string}
     * @memberof ProjectCreate
     */
    organizationId: string;
}

/**
 * Check if a given object implements the ProjectCreate interface.
 */
export function instanceOfProjectCreate(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "name" in value;
    isInstance = isInstance && "description" in value;
    isInstance = isInstance && "organizationId" in value;

    return isInstance;
}

export function ProjectCreateFromJSON(json: any): ProjectCreate {
    return ProjectCreateFromJSONTyped(json, false);
}

export function ProjectCreateFromJSONTyped(json: any, ignoreDiscriminator: boolean): ProjectCreate {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'name': json['name'],
        'description': json['description'],
        'organizationId': json['organization_id'],
    };
}

export function ProjectCreateToJSON(value?: ProjectCreate | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'name': value.name,
        'description': value.description,
        'organization_id': value.organizationId,
    };
}

