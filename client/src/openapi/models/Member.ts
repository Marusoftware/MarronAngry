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
 * @interface Member
 */
export interface Member {
    /**
     * 
     * @type {string}
     * @memberof Member
     */
    id: string;
    /**
     * 
     * @type {boolean}
     * @memberof Member
     */
    isAdmin: boolean;
    /**
     * 
     * @type {string}
     * @memberof Member
     */
    userId: string;
}

/**
 * Check if a given object implements the Member interface.
 */
export function instanceOfMember(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "id" in value;
    isInstance = isInstance && "isAdmin" in value;
    isInstance = isInstance && "userId" in value;

    return isInstance;
}

export function MemberFromJSON(json: any): Member {
    return MemberFromJSONTyped(json, false);
}

export function MemberFromJSONTyped(json: any, ignoreDiscriminator: boolean): Member {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': json['id'],
        'isAdmin': json['is_admin'],
        'userId': json['user_id'],
    };
}

export function MemberToJSON(value?: Member | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'id': value.id,
        'is_admin': value.isAdmin,
        'user_id': value.userId,
    };
}

