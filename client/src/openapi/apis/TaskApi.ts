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


import * as runtime from '../runtime';
import type {
  HTTPValidationError,
  Task,
  TaskCreate,
  TaskUpdate,
} from '../models';
import {
    HTTPValidationErrorFromJSON,
    HTTPValidationErrorToJSON,
    TaskFromJSON,
    TaskToJSON,
    TaskCreateFromJSON,
    TaskCreateToJSON,
    TaskUpdateFromJSON,
    TaskUpdateToJSON,
} from '../models';

export interface TaskCreateRequest {
    taskCreate: TaskCreate;
}

export interface TaskDeleteRequest {
    taskId: string;
}

export interface TaskGetRequest {
    prjId: string;
}

export interface TaskUpdateRequest {
    taskId: string;
    taskUpdate: TaskUpdate;
}

/**
 * 
 */
export class TaskApi extends runtime.BaseAPI {

    /**
     * Create
     */
    async taskCreateRaw(requestParameters: TaskCreateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Task>> {
        if (requestParameters.taskCreate === null || requestParameters.taskCreate === undefined) {
            throw new runtime.RequiredError('taskCreate','Required parameter requestParameters.taskCreate was null or undefined when calling taskCreate.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        if (this.configuration && this.configuration.accessToken) {
            // oauth required
            headerParameters["Authorization"] = await this.configuration.accessToken("OAuth2PasswordBearer", []);
        }

        const response = await this.request({
            path: `/task/`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: TaskCreateToJSON(requestParameters.taskCreate),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => TaskFromJSON(jsonValue));
    }

    /**
     * Create
     */
    async taskCreate(requestParameters: TaskCreateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Task> {
        const response = await this.taskCreateRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Delete
     */
    async taskDeleteRaw(requestParameters: TaskDeleteRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<any>> {
        if (requestParameters.taskId === null || requestParameters.taskId === undefined) {
            throw new runtime.RequiredError('taskId','Required parameter requestParameters.taskId was null or undefined when calling taskDelete.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.accessToken) {
            // oauth required
            headerParameters["Authorization"] = await this.configuration.accessToken("OAuth2PasswordBearer", []);
        }

        const response = await this.request({
            path: `/task/{task_id}`.replace(`{${"task_id"}}`, encodeURIComponent(String(requestParameters.taskId))),
            method: 'DELETE',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.TextApiResponse(response) as any;
    }

    /**
     * Delete
     */
    async taskDelete(requestParameters: TaskDeleteRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<any> {
        const response = await this.taskDeleteRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Get
     */
    async taskGetRaw(requestParameters: TaskGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<Task>>> {
        if (requestParameters.prjId === null || requestParameters.prjId === undefined) {
            throw new runtime.RequiredError('prjId','Required parameter requestParameters.prjId was null or undefined when calling taskGet.');
        }

        const queryParameters: any = {};

        if (requestParameters.prjId !== undefined) {
            queryParameters['prj_id'] = requestParameters.prjId;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.accessToken) {
            // oauth required
            headerParameters["Authorization"] = await this.configuration.accessToken("OAuth2PasswordBearer", []);
        }

        const response = await this.request({
            path: `/task/`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(TaskFromJSON));
    }

    /**
     * Get
     */
    async taskGet(requestParameters: TaskGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<Task>> {
        const response = await this.taskGetRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Update
     */
    async taskUpdateRaw(requestParameters: TaskUpdateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Task>> {
        if (requestParameters.taskId === null || requestParameters.taskId === undefined) {
            throw new runtime.RequiredError('taskId','Required parameter requestParameters.taskId was null or undefined when calling taskUpdate.');
        }

        if (requestParameters.taskUpdate === null || requestParameters.taskUpdate === undefined) {
            throw new runtime.RequiredError('taskUpdate','Required parameter requestParameters.taskUpdate was null or undefined when calling taskUpdate.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        if (this.configuration && this.configuration.accessToken) {
            // oauth required
            headerParameters["Authorization"] = await this.configuration.accessToken("OAuth2PasswordBearer", []);
        }

        const response = await this.request({
            path: `/task/{task_id}`.replace(`{${"task_id"}}`, encodeURIComponent(String(requestParameters.taskId))),
            method: 'PATCH',
            headers: headerParameters,
            query: queryParameters,
            body: TaskUpdateToJSON(requestParameters.taskUpdate),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => TaskFromJSON(jsonValue));
    }

    /**
     * Update
     */
    async taskUpdate(requestParameters: TaskUpdateRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Task> {
        const response = await this.taskUpdateRaw(requestParameters, initOverrides);
        return await response.value();
    }

}