import streamlit as st
import re

# Define the menu
menu = {
    "Appetizers": {
        "Garlic Bread": {"price": 5.99, "description": "Toasted bread with garlic butter", "allergens": ["gluten", "dairy"]},
        "Mozzarella Sticks": {"price": 7.99, "description": "Breaded and fried mozzarella", "allergens": ["gluten", "dairy"]},
    },
    "Main Courses": {
        "Margherita Pizza": {"price": 12.99, "description": "Classic pizza with tomato and mozzarella", "allergens": ["gluten", "dairy"]},
        "Chicken Alfredo": {"price": 15.99, "description": "Creamy pasta with grilled chicken", "allergens": ["gluten", "dairy"]},
    },
    "Desserts": {
        "Tiramisu": {"price": 6.99, "description": "Coffee-flavored Italian dessert", "allergens": ["gluten", "dairy", "eggs"]},
        "Chocolate Brownie": {"price": 5.99, "description": "Warm chocolate brownie with vanilla ice cream", "allergens": ["gluten", "dairy", "eggs"]},
    },
    "Drinks": {
        "Soda": {"price": 2.99, "description": "Choice of Coca-Cola, Sprite, or Fanta", "allergens": []},
        "Iced Tea": {"price": 2.99, "description": "Freshly brewed iced tea", "allergens": []},
    }
}

# Initialize or get the order from session state
if "order" not in st.session_state:
    st.session_state.order = []

def get_intent(user_input):
    user_input = user_input.lower()
    if re.search(r'\b(hi|hello|hey)\b', user_input):
        return "GREETING"
    elif re.search(r'\b(menu|what.+offer|what.+available)\b', user_input):
        return "MENU_INQUIRY"
    elif re.search(r'\b(order|add|get)\b', user_input):
        return "ORDER_INTENT"
    elif re.search(r'\b(ingredient|allerg)\b', user_input):
        return "INGREDIENT_INQUIRY"
    elif re.search(r'\b(hour|open|close)\b', user_input):
        return "HOURS_INQUIRY"
    elif re.search(r'\b(location|address|where)\b', user_input):
        return "LOCATION_INQUIRY"
    elif re.search(r'\b(view|show|check).+(order|cart)\b', user_input):
        return "VIEW_ORDER"
    else:
        return "UNKNOWN"

def extract_menu_items(user_input):
    items = []
    for category in menu:
        for item in menu[category]:
            if item.lower() in user_input.lower():
                items.append(item)
    return items

def get_bot_response(user_input):
    intent = get_intent(user_input)
    
    if intent == "GREETING":
        return "Hello! Welcome to our restaurant. How can I assist you today?"
    
    elif intent == "MENU_INQUIRY":
        return "Our menu categories are: " + ", ".join(menu.keys()) + ". Which category would you like to see?"
    
    elif intent == "ORDER_INTENT":
        items = extract_menu_items(user_input)
        if items:
            for item in items:
                st.session_state.order.append(item)
            return f"I've added {', '.join(items)} to your order. Anything else?"
        return "I'm sorry, I couldn't find that item in our menu. Can you please specify an item from our menu?"
    
    elif intent == "INGREDIENT_INQUIRY":
        items = extract_menu_items(user_input)
        if items:
            responses = []
            for item in items:
                for category in menu:
                    if item in menu[category]:
                        allergens = menu[category][item]['allergens']
                        responses.append(f"{item} contains: {', '.join(allergens)}" if allergens else f"{item} doesn't contain any common allergens.")
            return "\n".join(responses)
        return "I'm sorry, I couldn't find that item in our menu. Can you please specify an item from our menu?"
    
    elif intent == "HOURS_INQUIRY":
        return "We're open from 11 AM to 10 PM, seven days a week."
    
    elif intent == "LOCATION_INQUIRY":
        return "We're located at 123 Main Street, Anytown, USA."
    
    elif intent == "VIEW_ORDER":
        if st.session_state.order:
            return "Your current order: " + ", ".join(st.session_state.order)
        else:
            return "Your order is empty. Would you like to see our menu?"

    # Check for menu category inquiries
    for category in menu:
        if category.lower() in user_input.lower():
            return f"Here are our {category}:\n" + "\n".join([f"- {item}: ${menu[category][item]['price']} - {menu[category][item]['description']}" for item in menu[category]])

    return "I'm sorry, I didn't quite understand that. You can ask about our menu, place an order, inquire about ingredients, or ask about our hours and location. How can I help you?"

def main():
    st.title("🍽️ Restaurant Order Assistant")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        welcome_message = (
            "Welcome to our Restaurant Order Assistant! 👋\n\n"
            "I can help you with the following:\n"
            "- View our menu categories and items\n"
            "- Place an order\n"
            "- Provide information about ingredients and allergens\n"
            "- Answer questions about our hours and location\n"
            "- Show your current order\n\n"
            "How can I assist you today?"
        )
        st.session_state.messages.append({"role": "assistant", "content": welcome_message})

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Type your question or order here"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = get_bot_response(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display current order
    if st.session_state.order:
        st.sidebar.title("Your Order")
        for item in st.session_state.order:
            st.sidebar.write(f"- {item}")
        if st.sidebar.button("Clear Order"):
            st.session_state.order = []
            st.experimental_rerun()

if __name__ == "__main__":
    main()