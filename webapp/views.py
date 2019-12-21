from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.core.serializers import serialize
from django.http import JsonResponse
from .models import PolicyRule, Transaction
import requests
import time
import json

@api_view(['GET'])
def get_rules(request):
    try:
        # Grab all rules from database
        rules_list = PolicyRule.objects.all()
        
        # Create paginator 
        paginator = Paginator(rules_list, 5)
        # Grab current page number from URL
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1
        # Use the paginator to get current page
        try:
            rules = paginator.page(page)
        except:
            rules = paginator.page(paginator.num_pages)

        # Parse the paged rules to a proper format
        rules = [{'uid':rule.uid, 'maxAmount': rule.maxAmount, 'destinations': rule.destinations} for rule in rules]

        # Serialize the received rules into JSON format
        rules_json = json.dumps(rules)
       
        # Return a JSON response contained with the serialized data
        return JsonResponse(rules_json, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_rule(request, maxAmount, destinations, amountInUsd=False):
    try:
        # Convert parameters types
        amount = int(maxAmount)

        # Check if the amount 
        if amountInUsd:
            # Get the current exchange rate of our currency in USD
            usd = float(requests.get('https://blockchain.info/tobtc?currency=USD&value=1').text)

            # Set the correct value for the amount
            maxAmount = usd * maxAmount / 10e7

        # Check if the specified rule already exists
        if any(PolicyRule.objects.filter(maxAmount=maxAmount, destinations=destinations)):
            return JsonResponse("The specified rule already exists!", safe=False)

        # Create the new rule and insert save it
        rule = PolicyRule(uid=int(time.time()), maxAmount=maxAmount, destinations=destinations)
        rule.save()

        # Return JSON response indicating that the rule was added
        return JsonResponse("The specified rule has been successfully added", safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def del_rule(request, uid):
    try:
        # Search the specified rule
        rule = PolicyRule.objects.filter(uid=uid)

        # Check if the specified rule was found
        if rule.count() > 0:
            # Delete the rule 
            rule.delete()

            # Return the appropriate response            
            return JsonResponse('The given rule has been successfully deleted!', safe=False)
        else:
            return JsonResponse('The given rule cannot be found and therefore cannot be deleted', safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_rule(request, uid, maxAmount, destinations, amountInUsd=False):
    try:
        # Search the specified rule
        rule = PolicyRule.objects.filter(uid=uid)

        # Check if the specified rule was found
        if rule.count() > 0:
            # Check if the amount 
            if amountInUsd:
                # Get the current exchange rate of our currency in USD
                usd = float(requests.get('https://blockchain.info/tobtc?currency=USD&value=1').text)

                # Set the correct value for the amount
                maxAmount = usd * maxAmount

            # Update rule
            rule.update(maxAmount=maxAmount, destinations=destinations)

            # Return the appropriate response            
            return JsonResponse('The given rule has been successfully updated!', safe=False)
        else:
            return JsonResponse('The given rule cannot be found and therefore cannot be updated', safe=False)

    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_transactions(request, outgoing=None):
    try:
        # Grab the transactions from the database
        if outgoing != None:
            transactions = Transaction.objects.filter(outgoing=outgoing)
        else:
            transactions = Transaction.objects.all()
        print(outgoing, outgoing != None)

        # Serialize the received transactions into JSON format
        transactions_json = serialize('json', list(transactions))
        # Return a JSON response contained with the serialized data
        return JsonResponse(transactions_json, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_transaction(request, amount, destination):
    try:
        # Convert parameters types
        amount = int(amount)

        # Check if the specified amount or destination are invalid and return an indication of the problem if so 
        if amount <= 0:
            return JsonResponse('Amount must be bigger than 0, please refill the values accordingly', safe=False)
        elif destination.strip() == '':
            return JsonResponse('The given destination is empty, please refill the values accordingly', safe=False)

        # Create an empty parameter to store the max amount between all rules containing the 
        # Current destination
        maxAmountFound = -1

        # Grab all rules from database
        rules = PolicyRule.objects.all()

        # Filter all rules to ones who match the destination
        for rule in rules:
            # Split destinations by ',' and strip the strings from unnecessary whitespaces
            destinations = list(map(lambda x: x.strip(), rule.destinations.split(',')))
            
            # Check the given destination against the rule destinations and check if
            # the amount of the current rule is higher than the current maximum amount "found"
            if destination in destinations and rule.maxAmount > maxAmountFound:
                maxAmountFound = rule.maxAmount
        
        # Check if the given amount is allowed by the current rules
        allowed = amount <= maxAmountFound

        # Create and save the current transaction
        transaction = Transaction(amount=amount, destination=destination, outgoing=allowed)
        transaction.save()
        
        # Return the appropriate response
        if allowed:
            return JsonResponse('The transaction has been added and as been marked as outgoing (allowed) by the system', safe=False)
        else:
            return JsonResponse('The transaction has been rejected by the system', safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)