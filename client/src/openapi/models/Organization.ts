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
import type { Member } from './Member';
import {
    MemberFromJSON,
    MemberFromJSONTyped,
    MemberToJSON,
} from './Member';

/**
 * 
 * @export
 * @interface Organization
 */
export interface Organization {
    /**
     * 
     * @type {string}
     * @memberof Organization
     */
    id: string;
    /**
     * 
     * @type {string}
     * @memberof Organization
     */
    name: string;
    /**
     * 
     * @type {string}
     * @memberof Organization
     */
    description: string;
    /**
     * 
     * @type {Array<Member>}
     * @memberof Organization
     */
    members: Array<Member>;
}

/**
 * Check if a given object implements the Organization interface.
 */
export function instanceOfOrganization(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "id" in value;
    isInstance = isInstance && "name" in value;
    isInstance = isInstance && "description" in value;
    isInstance = isInstance && "members" in value;

    return isInstance;
}

export function OrganizationFromJSON(json: any): Organization {
    return OrganizationFromJSONTyped(json, false);
}

export function OrganizationFromJSONTyped(json: any, ignoreDiscriminator: boolean): Organization {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': json['id'],
        'name': json['name'],
        'description': json['description'],
        'members': ((json['members'] as Array<any>).map(MemberFromJSON)),
    };
}

export function OrganizationToJSON(value?: Organization | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'id': value.id,
        'name': value.name,
        'description': value.description,
        'members': ((value.members as Array<any>).map(MemberToJSON)),
    };
}
