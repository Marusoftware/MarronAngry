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
 * @interface TaskCreate
 */
export interface TaskCreate {
    /**
     * 
     * @type {string}
     * @memberof TaskCreate
     */
    name: string;
    /**
     * 
     * @type {string}
     * @memberof TaskCreate
     */
    description: string;
    /**
     * 
     * @type {Date}
     * @memberof TaskCreate
     */
    start: Date;
    /**
     * 
     * @type {Date}
     * @memberof TaskCreate
     */
    end: Date;
    /**
     * 
     * @type {string}
     * @memberof TaskCreate
     */
    projectId: string;
}

/**
 * Check if a given object implements the TaskCreate interface.
 */
export function instanceOfTaskCreate(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "name" in value;
    isInstance = isInstance && "description" in value;
    isInstance = isInstance && "start" in value;
    isInstance = isInstance && "end" in value;
    isInstance = isInstance && "projectId" in value;

    return isInstance;
}

export function TaskCreateFromJSON(json: any): TaskCreate {
    return TaskCreateFromJSONTyped(json, false);
}

export function TaskCreateFromJSONTyped(json: any, ignoreDiscriminator: boolean): TaskCreate {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'name': json['name'],
        'description': json['description'],
        'start': (new Date(json['start'])),
        'end': (new Date(json['end'])),
        'projectId': json['project_id'],
    };
}

export function TaskCreateToJSON(value?: TaskCreate | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'name': value.name,
        'description': value.description,
        'start': (value.start.toISOString()),
        'end': (value.end.toISOString()),
        'project_id': value.projectId,
    };
}

