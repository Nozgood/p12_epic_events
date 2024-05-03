import models
import errors
import controllers
import views


class MainController:
    def __init__(self, session, console):

        self.session = session
        self.view = views.MainView(console=console)
        self.collaborator = None

        self.collaborator_controller = controllers.CollaboratorController(
            session=session,
            view=views.CollaboratorView(console=console)
        )

        self.customer_controller = controllers.CustomerController(
            session=session,
            view=views.CustomerView(console=console)
        )

        self.deal_controller = controllers.DealController(
            session=session,
            view=views.DealView(console=console)
        )

        self.event_controller = controllers.EventController(
            session=session,
            view=views.EventView(console=console)
        )

    def run(self):
        self.view.input_welcome()
        running = True
        while running:
            menu_selection = self.view.display_main_menu()
            match menu_selection:
                case 0:
                    running = False
                case 1:
                    collaborator = None
                    try:
                        collaborator = self.collaborator_controller.login()
                    except ValueError as err:
                        self.view.display_error(err)
                        continue
                    self.set_collaborator_to_controllers(collaborator)
                    self.view.input_welcome_user(self.collaborator)
                    self.get_collaborator_main_menu()
                case _:
                    self.view.display_error(errors.ERR_MENU_INPUT)

    def set_collaborator_to_controllers(self, collaborator):
        self.collaborator = collaborator
        self.customer_controller.collaborator = collaborator
        self.deal_controller.collaborator = collaborator
        self.event_controller.collaborator = collaborator

    def get_collaborator_main_menu(self):
        running = True
        while running:
            menu_selection = (
                self.
                collaborator_controller.
                view.
                display_collaborator_menu(
                    self.collaborator.role
                )
            )
            if menu_selection == 0:
                running = False
                continue
            match self.collaborator.role:
                case models.CollaboratorRole.MANAGEMENT:
                    self.process_management_action(menu_selection)
                case models.CollaboratorRole.COMMERCIAL:
                    self.process_commercial_action(menu_selection)
                case models.CollaboratorRole.SUPPORT:
                    self.process_support_action(menu_selection)
                case _:
                    self.process_admin_action(menu_selection)

    def process_management_action(self, menu_selection):
        match menu_selection:
            case 1:
                self.customer_controller.list_customers()
            case 2:
                self.deal_controller.list_deals()
            case 3:
                pass
            case 4:
                pass
            case 5:
                self.collaborator_controller.manage_collaborators()
            case 6:
                try:
                    customer_to_manage = self.customer_controller.get_customer()
                    self.deal_controller.manage_deals(customer_to_manage)
                except ValueError as err:
                    self.view.display_error(err)
            case _:
                self.view.display_error(errors.ERR_MENU_INPUT)

    def process_commercial_action(self, menu_selection):
        match menu_selection:
            case 1:
                self.customer_controller.list_customers()
            case 2:
                self.deal_controller.list_deals()
            case 3:
                pass
            case 4:
                self.customer_controller.create_customer()
            case 5:
                self.customer_controller.update_customer()
            case 6:
                try:
                    customer_to_manage = self.customer_controller.get_customer(
                        self.collaborator
                    )
                    self.deal_controller.update_deal(customer_to_manage)
                except ValueError as err:
                    return self.view.display_error(err)

            case 7:
                pass
            case 8:
                pass
            case _:
                self.view.display_error(errors.ERR_MENU_INPUT)

    def process_support_action(self, menu_selection):
        if menu_selection > 5:
            self.view.display_error(errors.ERR_MENU_INPUT)
            return

    def process_admin_action(self, menu_selection):
        match menu_selection:
            case 1:
                pass
            case 2:
                self.customer_controller.update_customer()
            case 3:
                self.customer_controller.create_customer()
            case 4:
                self.collaborator_controller.create_collaborator()
            case _:
                self.view.display_error(errors.ERR_MENU_INPUT)
