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
 * @interface TaskUpdate
 */
export interface TaskUpdate {
    /**
     * 
     * @type {string}
     * @memberof TaskUpdate
     */
    name?: string;
    /**
     * 
     * @type {string}
     * @memberof TaskUpdate
     */
    description?: string;
    /**
     * 
     * @type {Date}
     * @memberof TaskUpdate
     */
    time?: Date;
    /**
     * 
     * @type {string}
     * @memberof TaskUpdate
     */
    projectId?: string;
}

/**
 * Check if a given object implements the TaskUpdate interface.
 */
export function instanceOfTaskUpdate(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function TaskUpdateFromJSON(json: any): TaskUpdate {
    return TaskUpdateFromJSONTyped(json, false);
}

export function TaskUpdateFromJSONTyped(json: any, ignoreDiscriminator: boolean): TaskUpdate {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'name': !exists(json, 'name') ? undefined : json['name'],
        'description': !exists(json, 'description') ? undefined : json['description'],
        'time': !exists(json, 'time') ? undefined : (new Date(json['time'])),
        'projectId': !exists(json, 'project_id') ? undefined : json['project_id'],
    };
}

export function TaskUpdateToJSON(value?: TaskUpdate | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'name': value.name,
        'description': value.description,
        'time': value.time === undefined ? undefined : (value.time.toISOString()),
        'project_id': value.projectId,
    };
}

