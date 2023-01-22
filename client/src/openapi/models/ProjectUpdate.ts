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
 * @interface ProjectUpdate
 */
export interface ProjectUpdate {
    /**
     * 
     * @type {string}
     * @memberof ProjectUpdate
     */
    name: string;
    /**
     * 
     * @type {string}
     * @memberof ProjectUpdate
     */
    description: string;
    /**
     * 
     * @type {string}
     * @memberof ProjectUpdate
     */
    organizationId: string;
}

/**
 * Check if a given object implements the ProjectUpdate interface.
 */
export function instanceOfProjectUpdate(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "name" in value;
    isInstance = isInstance && "description" in value;
    isInstance = isInstance && "organizationId" in value;

    return isInstance;
}

export function ProjectUpdateFromJSON(json: any): ProjectUpdate {
    return ProjectUpdateFromJSONTyped(json, false);
}

export function ProjectUpdateFromJSONTyped(json: any, ignoreDiscriminator: boolean): ProjectUpdate {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'name': json['name'],
        'description': json['description'],
        'organizationId': json['organization_id'],
    };
}

export function ProjectUpdateToJSON(value?: ProjectUpdate | null): any {
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

