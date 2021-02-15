import sys, os
import json
import urllib.parse
from oraRESTTools import *
import datetime
import time

def postData ( objectList, url ):
	for object in objectList:
		t, status, statusText = postRest( url, session, object, requestHeader, authorization, log )
		log.info('\t\t\tStatusCode: %s\t TotalTime: \t%s sec \t%s' % ( status, t, t ) )
		
	
def createWorkOrders( restCount, batchChunks ):
	log.info('\tCreating WorkOrders')
	start = getTime()
	workOrders = getExcelData( woFile, 'WorkOrders' )
	'''
	items = set( dict['InventoryItemId'] for dict in workOrders )
	itemsUrl = getUrl(url, 'itemsV2')
	query={ 'OrganizationCode': '405', 'ItemNumber':'ESB500003'}
	itemId, t, status, statusText, restCount = getRest( itemsUrl, session, payload, query, requestHeader, authorization, recordLimit, log, restCount, proxies)
	print(items)
	'''
	Id = 1
	
	partsList = []
	log.info('\t\t-->Getting Work Orders...')
	for wo in workOrders:
		workOrder={}
		workOrder['WorkOrderNumber'] = wo['WorkOrderNumber']
		workOrder['OrganizationCode'] = wo['OrganizationCode']
		workOrder['ItemNumber'] = wo['ItemNumber']
		workOrder['PlannedStartQuantity'] = wo['PlannedStartQuantity']
		workOrder['PlannedStartDate'] = wo['PlannedStartDate']
		workOrder['WorkDefinitionCode'] = wo['WorkDefinitionCode']
		workOrder['FirmPlannedFlag'] = wo['FirmPlannedFlag']
		workOrder['ExplosionFlag'] = 'true'
		parts = getParts(Id, getUrl( '','/workOrders'), 'create', workOrder)
		partsList.append(parts)
		Id += 1

	chunks = [int(batchChunks)]
	#print (partsList)
	
	for c in chunks:
		#print (c)
		log.info('\t\tUpdating %s WorkOrder Records in batches of %s' % (len(partsList), c))
		t, status, statusText, restCount = postBatchRest( url, session, partsList, c, authorization, log, restCount, proxies)
		#print ('%%%%%%%%%%%%%%%%%%%%', status, statusText)
		TotalTime = getTime() - start
		log.info('\t\tCreated WorkOrders %s REST calls in %s\tsec' % (restCount, TotalTime))
		
		
if __name__ == "__main__":
	'''	Set Variables, logging, and establish Session 	'''
	log = setLogging()
	variables = setVariables('psRest.xml')
	for key,val in variables.items():
		exec(key + '=val')	
	
	session, authorization, requestHeader, payload = scmAuth ( mfgUser, password )
	print ('\n\n!!!!', session, authorization)
	log.info('REST Server: %s' % ( url ))
	restCount = 0
	proxies = {'http': proxyServer,'https': proxyServer}
	
	createWorkOrders( restCount, batchChunks) 
	#createWorkOrdersSingle( restCount) 