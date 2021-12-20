import pytest
from datetime import datetime, timedelta, time
from Helper import BaseClass
import logging

class TestHelper:
    
    @pytest.fixture
    def helper(self, given_that):
        helper = BaseClass(
            None, BaseClass.__name__, None, None, None, None, None)
        
        given_that.passed_arg('debug').is_set_to('True')
        
        return helper
    
    def test__init_filter(self, given_that, helper, assert_that, caplog, time_travel):
        filterblacklist = list()
        filterblacklist.append("parentsbedroom_switch")
        filterblacklist.append("guest_room_switch")
        
        filterwhitelist = list()
        filterwhitelist.append("somewhitelistfilter")
        
        given_that.passed_arg('filter_blacklist').is_set_to(filterblacklist)
        given_that.passed_arg('filter_whitelist').is_set_to(filterwhitelist)
        
        helper._init_filter()
        
        assert helper._filter_blacklist == filterblacklist
        assert helper._filter_whitelist == filterwhitelist
        
    #no whitelist and not blacklist
    def test__init_filter_no_blacklist_no_whitelist(self, given_that, helper, assert_that, caplog, time_travel):
        
        helper._init_filter()
        
        assert helper._filter_blacklist == None
        assert helper._filter_whitelist == None
        

    def test__get_state_filtered_blacklist(self, given_that, helper, assert_that, caplog, time_travel):
        filterblacklist = list()
        filterblacklist.append("parents_room")
        filterblacklist.append("guest_room")
        
        given_that.passed_arg('filter_blacklist').is_set_to(filterblacklist)
        
        helper._init_filter()
        
        # Set initial state
        coverlist = ['living_room', 'guest_room', 'parents_room', 'kids_room']
        for cover in coverlist:
            given_that.state_of(f"cover.{cover}").is_set_to(
                "closed", {'friendly_name': f"{cover}", 'current_position': 0, 'value_id': cover})
        
        #build expected result
        coverlist = ['living_room','kids_room']
        statedict = dict()
        for cover in coverlist:
            attributesdict = dict()
            attributesdict.update({'friendly_name': f"{cover}", 'current_position': 0, 'value_id': cover})
            sdict = dict()
            sdict.update({"state": "closed", "attributes": attributesdict})
            statedict.update({f"cover.{cover}": sdict})
        
        filtered_statedict = helper._get_state_filtered()
        
        print(statedict)
        print(filtered_statedict)
        
        assert filtered_statedict == statedict        
        
    def test__get_state_filtered_whitelist(self, given_that, helper, assert_that, caplog, time_travel):
        
        filterwhitelist = list()
        filterwhitelist.append("living_room")
        
        given_that.passed_arg('filter_whitelist').is_set_to(filterwhitelist)
        
        helper._init_filter()
        
        # Set initial state
        coverlist = ['living_room', 'guest_room', 'parents_room', 'kids_room']
        for cover in coverlist:
            given_that.state_of(f"cover.{cover}").is_set_to(
                "closed", {'friendly_name': f"{cover}", 'current_position': 0, 'value_id': cover})
        
        #build expected result
        coverlist = ['living_room']
        statedict = dict()
        for cover in coverlist:
            attributesdict = dict()
            attributesdict.update({'friendly_name': f"{cover}", 'current_position': 0, 'value_id': cover})
            sdict = dict()
            sdict.update({"state": "closed", "attributes": attributesdict})
            statedict.update({f"cover.{cover}": sdict})
        
        filtered_statedict = helper._get_state_filtered()
        
        print(statedict)
        print(filtered_statedict)
        
        assert filtered_statedict == statedict        