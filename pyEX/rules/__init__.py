# -*- coding: utf-8 -*-
from functools import wraps
from ..common import _getJson, _postJson, _deleteJson, _raiseIfNotStr, PyEXception


def lookup(lookup='', token='', version=''):
    '''Pull the latest schema for data points, notification types, and operators used to construct rules.

    https://iexcloud.io/docs/api/#rules-schema

    Args:
        lookup (string); If a schema object has “isLookup”: true, pass the value key to /stable/rules/lookup/{value}. This returns all valid values for the rightValue of a condition.
        token (string); Access token
        version (string); API version

    Returns:
        dict: result
    '''
    _raiseIfNotStr(lookup)
    if lookup:
        return _getJson('rules/lookup/{}'.format(lookup), token, version, None)
    return _getJson('rules/schema', token, version, None)


@wraps(lookup)
def schema(token='', version=''):
    return lookup(token=token, version=version)


def create(rule, ruleName, ruleSet, type='any', existingId=None):
    '''This endpoint is used to both create and edit rules. Note that rules run be default after being created.

    Args:
        rule (Rule): rule object to create
        ruleName (str): name for rule
        ruleSet (str): Valid US symbol or the string ANYEVENT. If the string ANYEVENT is passed, the rule will be triggered for any symbol in the system. The cool down period for alerts (frequency) is applied on a per symbol basis.
        type (str): Specify either any, where if any condition is true you get an alert, or all, where all conditions must be true to trigger an alert. any is the default value
        existingId (Optional[str]): The id of an existing rule only if you are editing the existing rule


    conditions	array	Required An array of arrays. Each condition array will consist of three values; left condition, operator, right condition.

                        Ex: [ [‘latestPrice’, ‘>’, 200.25], [‘peRatio’, ‘<’, 20] ]
    outputs	array	Required An array of one object. The object’s schema is defined for each notification type, and is returned by the notificationTypes array in the /rules/schema endpoint.
                    Every output object will contain method (which should match the value key of the notificationType, and frequency which is the number of seconds to wait between alerts.

                    Ex: [ { method: ‘webhook’, url: ‘https://myserver.com/iexcloud-webhook’, frequency: 60 } ]
    additionalKeys	array	Optional. An array of schema data values to be included in alert message in addition to the data values in the conditions.

                            Ex: ['latestPrice', 'peRatio', 'nextEarningsDate']
    '''
    if type not in ('any', 'all'):
        raise PyEXception('type must be in (any, all). got: {}'.format(type))


def pause(ruleId, token='', version=''):
    '''You can control the output of rules by pausing and resume per rule id.

    Args:
        ruleId (str): The id of an existing rule to puase
    '''
    return _postJson('rules/pause', data={"ruleId": ruleId}, token=token, version=version)


def resume(ruleId, token='', version=''):
    '''You can control the output of rules by pausing and resume per rule id.

    Args:
        ruleId (str): The id of an existing rule to puase
    '''
    return _postJson('rules/resume', data={"ruleId": ruleId}, token=token, version=version)


def delete(ruleId, token='', version=''):
    '''You can delete a rule by using an __HTTP DELETE__ request. This will stop rule executions and delete the rule from your dashboard. If you only want to temporarily stop a rule, use the pause/resume functionality instead.

    Args:
        ruleId (str): The id of an existing rule to puase
    '''
    return _deleteJson('rules/{}'.format(ruleId), token=token, version=version)
